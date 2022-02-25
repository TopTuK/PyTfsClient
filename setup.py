from setuptools import setup

### Execute
# python setup.py sdist
# twine upload dist/*

setup(
    name='PyTfsClient',
    packages=['lib'],
    version='0.9',
    license='MIT',
    description='Microsoft Team Foundation Server Python Library is a Microsoft TFS API Python client that can work with Microsoft TFS workitems',
    url='https://github.com/TopTuK/PyTfsClient',
    author='TopTuK',
    author_email='cydoor88@gmail.com',
    download_url = 'https://github.com/TopTuK/PyTfsClient/archive/refs/tags/v0.2-beta.tar.gz',  
    install_requires=[
        'urljoin',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.8'
    ],
    keywords = ['TFS', 'AZURE', 'TFS API', 'Team Foundation Server'],   # Keywords that define your package best
    zip_safe=False
)