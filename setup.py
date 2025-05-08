from setuptools import find_packages,setup

setup(
    name = 'mcqgenerator',
    version= '0.0.1',
    author= 'shamshad',
    author_email='alam.shams.1996@gmail.com',
    install_requires = ["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain_community","langchain_openai"],
    packages=find_packages()
)