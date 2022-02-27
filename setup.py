import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='joi_skill_utils',
    version='0.0.38',
    author='Ty Seddon',
    author_email='ty.seddon@cognivista.com',
    description='Utility classes shared by multiple Mycroft Skills for Joi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/TySeddon/joi-skill-utils',
    project_urls = {
        "Bug Tracker": "https://github.com/TySeddon/joi-skill-utils/issues"
    },
    license='MIT',
    packages=['joi_skill_utils'],
    install_requires=[
        'requests',
        'munch',
        'pyyaml',
        'google-api-python-client',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'azure-ai-textanalytics==5.2.0b1',
        'azure-ai-language-questionanswering',
        'spotipy==2.19.0',
        'amcrest',
        'numpy',
        'pandas',
        'ifaddr'
    ],
)