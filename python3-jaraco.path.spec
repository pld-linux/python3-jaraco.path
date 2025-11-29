#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Miscellaneous path functions
Summary(pl.UTF-8):	Różne funkcje związane ze ścieżkami
Name:		python3-jaraco.path
Version:	3.7.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco-path/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco-path/jaraco_path-%{version}.tar.gz
# Source0-md5:	1e3e22665d2a4c58e632d99fa54b0967
URL:		https://pypi.org/project/jaraco.path/
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:61.2
BuildRequires:	python3-setuptools_scm >= 3.4.1
%if %{with tests}
BuildRequires:	python3-pytest >= 6
# lint only
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-enabler >= 2.2
#BuildRequires:	python3-pytest-mypy
#BuildRequires:	python3-pytest-ruff >= 0.2.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9.3
BuildRequires:	python3-rst.linker >= 1.9
#BuildRequires:	python3-sphinx-lint
BuildRequires:	sphinx-pdg-3 >= 3.5
%endif
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Miscellaneous path functions.

%description -l pl.UTF-8
Różne funkcje związane ze ścieżkami.

%package apidocs
Summary:	API documentation for Python jaraco.path module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jaraco.path
Group:		Documentation

%description apidocs
API documentation for Python jaraco.path module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jaraco.path.

%prep
%setup -q -n jaraco_path-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest jaraco tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst
%{py3_sitescriptdir}/jaraco/path.py
%{py3_sitescriptdir}/jaraco/__pycache__/path.cpython-*.py[co]
%{py3_sitescriptdir}/jaraco_path-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
