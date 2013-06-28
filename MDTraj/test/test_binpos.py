# Copyright 2012 mdtraj developers
#
# This file is part of mdtraj
#
# mdtraj is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# mdtraj is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# mdtraj. If not, see http://www.gnu.org/licenses/.

"""
Test the cython binpos module

Note, this file cannot be located in the binpos subdirectory, because that
directory is not a python package (it has no __init__.py) and is thus tests
there are not discovered by nose
"""
import tempfile, os
import numpy as np

from mdtraj import io, binpos
from mdtraj import DCDTrajectoryFile, BINPOSTrajectoryFile
from mdtraj.testing import get_fn, eq, DocStringFormatTester

TestDocstrings = DocStringFormatTester(binpos, error_on_none=True)


# frame0.binpos was generated from frame0.dcd using
# VMD. The binpos file has one more frame than the dcd file
# because VMD also saved the PDB coordinates
fn_binpos = get_fn('frame0.binpos')
fn_dcd = get_fn('frame0.dcd')

temp = tempfile.mkstemp(suffix='.binpos')[1]
def teardown_module(module):
    """remove the temporary file created by tests in this file
    this gets automatically called by nose"""
    os.unlink(temp)

def test_read_0():
    with BINPOSTrajectoryFile(fn_binpos) as f:
        xyz = f.read()
    with DCDTrajectoryFile(fn_dcd) as f:
        xyz2 = f.read()[0]
    xyz3 = io.loadh(get_fn('frame0.binpos.h5'), 'xyz')

    yield lambda: eq(xyz[1:], xyz2)
    yield lambda: eq(xyz, xyz3)


def test_read_1():
    with BINPOSTrajectoryFile(fn_binpos, chunk_size_multiplier=0.5) as f:
        xyz = f.read()
    with DCDTrajectoryFile(fn_dcd) as f:
        xyz2 = f.read()[0]
    xyz3 = io.loadh(get_fn('frame0.binpos.h5'), 'xyz')

    yield lambda: eq(xyz[1:], xyz2)
    yield lambda: eq(xyz, xyz3)


def test_read_2():
    with BINPOSTrajectoryFile(fn_binpos, chunk_size_multiplier=10) as f:
        xyz = f.read()
    with DCDTrajectoryFile(fn_dcd) as f:
        xyz2 = f.read()[0]
    xyz3 = io.loadh(get_fn('frame0.binpos.h5'), 'xyz')

    yield lambda: eq(xyz[1:], xyz2)
    yield lambda: eq(xyz, xyz3)


def test_write_1():
    xyz = np.array(np.random.randn(500, 10, 3), dtype=np.float32)
    with BINPOSTrajectoryFile(temp, 'w') as f:
        f.write(xyz)


    xyz2 = BINPOSTrajectoryFile(temp).read()
    eq(xyz, xyz2)