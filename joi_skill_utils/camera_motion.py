from munch import munchify
from datetime import datetime, timedelta
import asyncio
from asyncio import Event
from typing import AsyncIterator
import sys
import pandas as pd
from mycroft.messagebus import Message

class MotionDetection():

    def __init__(self, camera, loop, log, message_bus=None) -> None:
        self.camera = camera
        self.log = log
        self.message_bus = message_bus
        self.is_done = False
        self.is_motion = False
        self.cancellation_event = asyncio.Event(loop=loop)

    def build_motion_event(self,event_name):
        return munchify({
            'Event':event_name,
            'DateTime':datetime.utcnow()
        })

    def build_event_obj(self, event_str):
        if "Code=VideoMotion" in event_str:
            if "action=Start" in event_str:
                return self.build_motion_event('MotionStart')
            elif "action=Stop" in event_str:
                return self.build_motion_event('MotionStop')
            else:
                return None
        else:
            return None

    def _start(self):
        self.is_done = False
        self.is_motion = False

    def _stop(self):
        self.is_done = True

    def check_done(self):
        return self.is_done

    async def cancellable_aiter(self, async_iterator: AsyncIterator, cancellation_event: Event) -> AsyncIterator:
        cancellation_task = asyncio.create_task(cancellation_event.wait())
        result_iter = async_iterator.__aiter__()
        while not cancellation_event.is_set():
            next_result_task = asyncio.create_task(result_iter.__anext__())
            done, pending = await asyncio.wait(
                [cancellation_task, next_result_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            for done_task in done:
                if done_task == cancellation_task:
                    # clean up the async iterator
                    self.log.info("cleaning up async iterator")
                    next_result_task.cancel()
                    try:
                        await result_iter.aclose()
                    except Exception as error:
                        pass                        
                    self.log.info("cleaned up async iterator")

                    break
                else:
                    yield done_task.result()
            
    def _cancel(self, cancellation_event):
        self.log.info("Sending Cancel Signal")
        cancellation_event.set()
        self.log.info("Sent Cancel Signal")

    def cancel(self):
        self._cancel(self.cancellation_event)

    async def read_camera_motion_async(self, seconds_length):
        self.log.info("read_camera_motion_async")
        # setup cancellation after specified number of seconds
        self.cancellation_event.clear()
        loop = asyncio.get_event_loop()
        cancelTimer = loop.call_later(seconds_length, self._cancel, self.cancellation_event)

        self._start()

        # initialize event collection
        start_time = datetime.utcnow()
        motion_events = []
        motion_event_pairs = []
        last_event = None
        if bool(self.camera.is_motion_detected):
            starting_event = self.build_motion_event('MotionStart')
            motion_events.append(starting_event)
            last_event = starting_event
        else:        
            starting_event = self.build_motion_event('MotionStop')
            motion_events.append(starting_event)
            last_event = starting_event

        self.is_motion = last_event.Event == "MotionStart"

        # get events until number of seconds expire
        async_iter = self.camera.async_event_stream("VideoMotion")
        async for event_str in self.cancellable_aiter(async_iter, self.cancellation_event):
            current_event = self.build_event_obj(event_str)
            motion_events.append(current_event)
            if last_event and last_event.Event == "MotionStart" and current_event.Event == "MotionStop":
                motion_event_pairs.append((last_event, current_event))
            if last_event and last_event.Event == current_event.Event:
                pass # ignore this duplicate event
            else:
                last_event = current_event   
                if self.message_bus:
                    self.message_bus.emit(Message("skill.joi-skill-utils.motion_event", 
                                data={
                                        'event':last_event.Event, 
                                        'datetime':last_event.DateTime.isoformat()
                                }))
            self.is_motion = last_event.Event == "MotionStart"

        cancelTimer.cancel() # cancel the timer that would cancel this

        # end event collection
        ending_event=self.build_motion_event('End')
        if last_event and last_event.Event == "MotionStart":
            motion_event_pairs.append((last_event, ending_event))
        end_time = datetime.utcnow()

        self.log.info("read_camera_motion_async - DONE")
        self._stop()
        return (start_time, end_time, motion_event_pairs)


    def build_motion_history(self, start_time, end_time, motion_event_pairs):
        num_of_seconds = (end_time-start_time).seconds
        self.log.info(f"{start_time} to {end_time}.  {num_of_seconds} seconds.")

        history = []
        for current_time in (start_time + timedelta(seconds=n) for n in range(num_of_seconds)):
            self.is_motion = bool([p for p in motion_event_pairs if p[0].DateTime <= current_time <= p[1].DateTime])
            #print(f"{'X' if self.is_motion else '-'}", end='')
            history.append(int(self.is_motion))
        #sys.stdout.flush()        
        return history

    def build_rolling_history(self, history, window_size):
        series = pd.Series(history)
        return series.rolling(window_size).sum().apply(lambda o: o/window_size).fillna(0).tolist()

    def create_motion_report(self, start_time, end_time, motion_event_pairs):
        history = self.build_motion_history(start_time, end_time, motion_event_pairs)
        pairs = [(p[0].DateTime.isoformat(), p[1].DateTime.isoformat()) for p in motion_event_pairs]
        report = {
            'start_time':start_time.isoformat(),
            'end_time':end_time.isoformat(),
            'num_of_seconds': (end_time-start_time).seconds,
            'motion_event_pairs': pairs,
            'history': history,
            'rolling_history_5sec': self.build_rolling_history(history,5),
            'rolling_history_10sec': self.build_rolling_history(history,10),
            'percent': round(sum(history)/len(history),2) if history else None
        }
        self.log.info(report)
        return munchify(report)

    async def report_loop(self):
        while True:
            print(f"{'X' if self.is_motion else '-'}", end='')
            sys.stdout.flush()
            await asyncio.sleep(1)
            if self.is_done:
                break

    async def wait_complete(self):
        while True:
            await asyncio.sleep(1)
            if self.is_done:
                break
