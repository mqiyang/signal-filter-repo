import numpy as np


def get_cubefname(molecule, ftype, t):
    fname = molecule + '.' + ftype + '.{:010d}'.format(t) +'.cube'
    return fname


def get_matfname(molecule, t, dtype1, dtype2, spin):
    """
    get the fname for read in the mat files
    molecule: molecule shown in the matfnames
    t       : time step (it)
    dtype1  : "pmat" or "dpmat"
    dtype2  : "re" or "im"
    spin    : "alpha" or "beta"
    """
    fname = molecule+'.'+ dtype1 + '_' + dtype2 + '_' + spin+'.{:08d}'.format(t) + '.dat'
    return fname


def read_mat(matfname):
    with open(matfname, 'r') as f:
        header = f.readline()
        if ('[fil]' in header):
            raise Exception("data has already been filtered")
        nao = f.readline()
        data_str = np.array(f.readline().split())
        data = data_str.astype(float)
    return header, nao, data


def write_mat(header, nao, data, matfname, cutoff):
    header = header.strip() + " [fil] with {0:.2e} \n".format(cutoff) 
    with open(matfname, 'w') as f:
        f.write(header)
        f.write(nao)
        for i in range(data.shape[0]):
            f.write("{0: .8E}".format(data[i]))
            f.write(" ")
                    

def read_1d_file(fname):
    data = np.genfromtxt(fname)
    return np.array(data[:,0]), np.array(data[:,1] )


def write_1d_file(x, y, fname):
    with open (fname, 'w') as f:
        for xa, ya in zip(x,y):
            f.write("{0:.8E}\t {1:.8E}\n".format(xa, ya))


def au2angs(au_vals):
    return au_vals *  0.529177249


def read_hline(cube):
    """
    read head line (the ones with voxel information)
    return the voxel element
    """
    hline = cube.readline().strip().split()
    return int(hline[0]), np.array(list(map(float, hline[1:])))


def read_cube(fname, unit='au'):
    """
    read the provided cube file
    return the volumetric values and the metadata
    contains the voxel information
    unit is the targeted unit
    """
    meta = {}
    with open(fname, 'r') as cube:
        meta['firstline'] = cube.readline()
        meta['secondline'] = cube.readline()
        natm, meta['orig'] = read_hline(cube)
        nx, meta['xvec'] = read_hline(cube)
        ny, meta['yvec'] = read_hline(cube)
        nz, meta['zvec'] = read_hline(cube)
        meta['atoms'] = [read_hline(cube) for atm in range(natm)]
        if (unit == 'angs'):
            if ("angs" in meta['firstline']):
                raise Exception("data has already been converted into Angs")
            meta['orig'] = au2angs(meta['orig'])
            meta['xvec'] = au2angs(meta['xvec'])
            meta['yvec'] = au2angs(meta['yvec'])
            meta['zvec'] = au2angs(meta['zvec'])
            for atm in range(natm):
                meta['atoms'][atm][1][1:] =  au2angs(meta['atoms'][atm][1][1:])
            meta['firstline'] = '#'+ meta['firstline']
        data = np.empty((nx*ny*nz))
        # nx *= -1
        # ny *= -1
        # nz *= -1
        i = 0  # to count for total index
        for line in cube:
            for val in line.strip().split():
                data[i] = val   # float(val)
                i += 1
        # data = np.reshape(data, (nx, ny, nz))
        return nx, ny, nz, data, meta


def putline(*args):
    """
    Generate a line to be written to a cube file where
    the first field is an int and the remaining fields are floats.
    params:
        *args: first arg is formatted as int and remaining as floats
    returns: formatted string to be written to file with trailing newline
    """
    s = "{0:^ 8d}".format(args[0])
    s += "".join("{0:< 12.6f}".format(arg) for arg in args[1:])
    return s + "\n"


def write_cube(data, meta, fname):
    """
    write the density difference into a new file
    """
    with open(fname, 'w') as f:
        f.write(meta['firstline'])
        f.write(meta['secondline'])
        natm = len(meta['atoms'])
        nx, ny, nz = data.shape
        f.write(putline(natm, *meta['orig']))
        f.write(putline(nx, *meta['xvec']))
        f.write(putline(ny, *meta['yvec']))
        f.write(putline(nz, *meta['zvec']))
        for atom_mass, atom_pos in meta['atoms']:
            f.write(putline(atom_mass, *atom_pos))
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if (i or j or k) and k % 6 == 0:
                        f.write("\n")
                    f.write(" {0: .8E}".format(data[i, j, k]))



def write_file(data, meta, fname, outtype):
    """
    write the density difference into a new file
    """
    with open(fname, 'w') as f:
        f.write(meta['firstline'])
        f.write(meta['secondline'])
        natm = len(meta['atoms'])
        nx, ny, nz = data.shape
        f.write(putline(natm, *meta['orig']))
        f.write(putline(nx, *meta['xvec']))
        f.write(putline(ny, *meta['yvec']))
        f.write(putline(nz, *meta['zvec']))
        for atom_mass, atom_pos in meta['atoms']:
            f.write(putline(atom_mass, *atom_pos))
        if (outtype == "real"):
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        if (i or j or k) and k % 6 == 0:
                            f.write("\n")
                        f.write(" {0: .8E}".format(np.real(data[i, j, k])))
                            
        if (outtype == "imag"):
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        if (i or j or k) and k % 6 == 0:
                            f.write("\n")
                        f.write(" {0: .8E}".format(np.imag(data[i, j, k])))

        if (outtype == "abs"):
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        if (i or j or k) and k % 6 == 0:
                            f.write("\n")
                        f.write(" {0: .8E}".format(np.abs(data[i, j, k])))
