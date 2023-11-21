python_sources(name="lib")

resources(name="py.typed", sources=["py.typed"])

python_distribution(
    name="dist",
    dependencies=[":lib", ":py.typed"],
    wheel=True,
    sdist=True,
    provides=setup_py(
        name="era_5g_server",
        version="0.1.0",
        description="Barebones of 5G-ERA Network Applications",
        author="Michal Kapinus",
        author_email="ikapinus@fit.vutbr.cz",
        license="LGPL",
        python_requires=">=3.8",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: OS Independent",
            "Intended Audience :: Developers",
        ],
    ),
)
