import setuptools
with open(r'README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='pylolzapi',
	version='0.0.2',
	author='urlykkz',
	author_email='padreyonez@gmail.com',
	description='Python Wrapper for lolz.guru API',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['pylolzapi'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=['requests~=2.28.1\n', 'DateTime~=4.7\n', 'pydantic~=1.9.1'],
	python_requires='>=3.6',
	package_data={
		"pylolzapi": ['api/*.py', 'utils/*.py', 'types/*.py']
	},
)
