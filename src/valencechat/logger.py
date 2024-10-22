from os.path import join

def write_to_dir(information, datadir, session_id):
    fout = join(datadir, 'user-'+session_id+'.conversation.txt')
    with open(fout, 'a') as f:
        f.write(information+'\n')
