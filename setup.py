from setuptools import setup, find_packages

setup(
    name = 'django-geartracker',
    packages = find_packages(),
    version = '0.2',
    description = 'An inventory system for wilderness travel gear.',
    author = 'Peter Hogg',
    author_email = 'peter@havenaut.net',
    url = 'https://github.com/pigmonkey/django-geartracker',
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
    ],
    long_description = open('README.md').read(),
    include_package_data = True,
    zip_safe=False,
    install_requires = ['pil',
                        'django-taggit',
                        'django-taggit-templatetags',
                        'sorl-thumbnail',],
)
