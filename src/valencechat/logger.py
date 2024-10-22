from os.path import join

def write_to_dir(information, datadir, session):
    fout = join(datadir, 'user-'+session+'.conversation.txt')
    with open(fout, 'a') as f:
        f.write(information+'\n')
