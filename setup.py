from setuptools import setup, find_packages

### https://packaging.python.org/en/latest/tutorials/packaging-projects/
### Execute
# python setup.py sdist
# twine upload dist/*

# https://docs.python.org/3/distutils/setupscript.html
setup(
    name='PyTfsClient',
    version='1.0',
    license='MIT',
    description='Python Microsoft Team Foundation Server Library is a  client that can work with Microsoft TFS workitems',
    url='https://github.com/TopTuK/PyTfsClient',
    author='TopTuK',
    author_email='cydoor88@gmail.com',
    # download_url = 'https://github.com/TopTuK/PyTfsClient/archive/refs/tags/v0.2-beta.tar.gz',  
    install_requires=[
        'urljoin',
        'requests'
    ],
    #package_dir={"": ""},
    #packages=find_packages(where="lib"),
    packages=["pytfsclient"],
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.8'
    ],
    keywords = ['TFS', 'AZURE', 'TFS API', 'Team Foundation Server'],   # Keywords that define your package best
    zip_safe=False
)