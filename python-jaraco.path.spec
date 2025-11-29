#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-jaraco.path.spec)

Summary:	Miscellaneous path functions
Summary(pl.UTF-8):	Różne funkcje związane ze ścieżkami
Name:		python-jaraco.path
# keep 2.x here for python2 support
Version:	2.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco-path/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco-path/jaraco.path-%{version}.tar.gz
# Source0-md5:	4a4bcb98a1088eb2dc6b3113e5129b7b
URL:		https://pypi.org/project/jaraco.path/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:34.4
BuildRequires:	python-setuptools_scm >= 1.15
%if %{with tests}
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-flake8
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:34.4
BuildRequires:	python3-setuptools_scm >= 1.15
%if %{with tests}
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-flake8
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-jaraco.packaging >= 3.2
BuildRequires:	python-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-jaraco
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Miscellaneous path functions.

%description -l pl.UTF-8
Różne funkcje związane ze ścieżkami.

%package -n python3-jaraco.path
Summary:	Miscellaneous path functions
Summary(pl.UTF-8):	Różne funkcje związane ze ścieżkami
Group:		Libraries/Python
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.5

%description -n python3-jaraco.path
Miscellaneous path functions.

%description -n python3-jaraco.path -l pl.UTF-8
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
%setup -q -n jaraco.path-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_flake8 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_flake8 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
# local "jaraco" shadows system one; make jaraco.packaging.sphinx available locally
install -d build-2-docs
cp -pr build-2/lib/jaraco build-2-docs/jaraco
ln -sf %{py_sitescriptdir}/jaraco/packaging build-2-docs/jaraco/packaging

PYTHONPATH=$(pwd)/build-2-docs \
sphinx-build-2 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

# packaged in python-jaraco.spec
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/jaraco/__init__.py*
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__init__.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__pycache__/__init__.*.py*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/jaraco/path.py[co]
%{py_sitescriptdir}/jaraco.path-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-jaraco.path
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/jaraco/path.py
%{py3_sitescriptdir}/jaraco/__pycache__/path.cpython-*.py[co]
%{py3_sitescriptdir}/jaraco.path-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
