import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="movie_ticket_price_comparison",
    version="1.0.0",
    author="Sendhil",
    author_email="sendhildz@gmail.com",
    description="Movie Ticket Price Comparison",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sendhilg/movie-ticket-price-comparison",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
