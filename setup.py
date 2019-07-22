import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='metaweather',
    version='0.1.0',
    author='Maxime Barbet',
    author_email='maxibarbet@gmail.com',
    description='Display weather by location with metaweather api',
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/drscreener/software/valmul',
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'Requests'
    ],
    entry_points='''
        [console_scripts]
        metaweather=metaweather.metaweather:cli
    ''',
)