from setuptools import setup, find_packages

### https://packaging.python.org/en/latest/tutorials/packaging-projects/
### Execute
# python setup.py sdist
# twine upload dist/*

# https://docs.python.org/3/distutils/setupscript.html
setup(
    name='PyTfsClient',
    version='1.10.0',
    license='MIT',
    description='Python Microsoft Team Foundation Server Library is a  client that can work with Microsoft TFS workitems',
    url='https://github.com/TopTuK/PyTfsClient',
    author='TopTuK',
    author_email='cydoor88@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src', include=['pytfsclient*'], exclude=['.test', '*.test', 'test', 'test*', 'test.*', 'pytest.ini']),
    include_package_data=True,
    install_requires=[
        'urljoin',
        'requests',
        'requests_ntlm',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.8'
    ],
    keywords = ['TFS', 'AZURE', 'TFS API', 'Team Foundation Server'],   # Keywords that define your package best
    zip_safe=False
)