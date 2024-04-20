# run https://github.com/jwfoley/bioanalyzeR/ in Python

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr, isinstalled

# Enable automatic conversion between R data frames and pandas DataFrames
pandas2ri.activate()

def install_r_package(package_name, source_url=None):
    """
    Install an R package if it is not already installed.
    """
    if not isinstalled(package_name):
        if source_url:
            robjects.r(f'install.packages("{source_url}", repos=NULL)')
        else:
            robjects.r(f'install.packages("{package_name}", dependencies=TRUE)')
        print(f"Installed {package_name}")
    else:
        print(f"{package_name} is already installed.")

def ensure_packages_installed(packages):
    """
    Ensure that all R packages are installed.
    """
    for package, url in packages.items():
        install_r_package(package, url)

def load_r_package(package_name):
    """
    Load an R package using importr, assuming it is already installed.
    """
    try:
        return importr(package_name)
    except Exception as e:
        print(f"Error loading R package {package_name}: {str(e)}")
        return None

def load_r_packages(packages):
    """
    Load multiple R packages.
    """
    return {package: load_r_package(package) for package in packages}

def process_electrophoresis_data(filename, data_part):
    """
    Process electrophoresis data from an XML file and return a pandas DataFrame of the specified part.
    """
    r_code = f'''
    library(bioanalyzeR)
    data <- read.electrophoresis("{filename}")
    data_part <- data${data_part}
    '''
    
    try:
        robjects.r(r_code)
        # Convert the specified part of the data to a pandas DataFrame using the new conversion method
        data_part_df = rpy2py(robjects.r['data_part'])
        return data_part_df
    except Exception as e:
        print("Error processing electrophoresis data:", e)
        return None

# Configuration: Packages to install
required_packages = {
    'XML': "https://cran.r-project.org/src/contrib/XML_3.99-0.16.1.tar.gz",
    'base64enc': None,
    'plyr': None,
    'ggplot2': None,
    'dplyr': None,
    'bioanalyzeR': "https://github.com/jwfoley/bioanalyzeR/releases/download/v0.10.1/bioanalyzeR_0.10.1-no_data.tar.gz"
}

# Load R packages
ensure_packages_installed(required_packages)
r_packages = load_r_packages(required_packages.keys())

# Example usage
filename = 'filename.xml'
data_part = 'samples'  # Could also be 'peaks' or any other valid part of XML file
df = process_electrophoresis_data(filename, data_part)
if df is not None:
    print(df)
