print("Booting Up Python")
import builtins
import micropip
from pyodide import to_js

sav = None
input_filename = "/input.sav"
output_filename = "/output.sav"

async def install_deps():
    await micropip.install('setuptools')
    import setuptools
    # await micropip.install('https://softwareprocess.es/2022/ttwl_cli_saveedit-0.0.5-py3-none-any.whl')
    await micropip.install('ttwl-cli-saveedit')
    import ttwlsave
    from ttwlsave.ttwlsave import TTWLSave
    print("Done deps")

async def get_binary_url(url):
    from js import fetch
    from io import BytesIO
    response = await fetch(url)
    js_buffer = await response.arrayBuffer()
    return BytesIO(js_buffer.to_py()).read()

async def save_binary_url(url, filename):
    data = await get_binary_url(url)
    with open(filename,"wb") as fd:
        fd.write(data)
    
async def load_example():
    global sav
    import ttwlsave
    from ttwlsave.ttwlsave import TTWLSave    
    await save_binary_url("https://softwareprocess.es/2022/example-ttwl.sav",input_filename)
    sav = TTWLSave("/input.sav")
    print(sav.get_char_name())
    return sav.get_char_name()

def wrap_io(f):
    import io
    import sys
    out = io.StringIO()
    oldout = sys.stdout
    olderr = sys.stderr
    sys.stdout = sys.stderr = out
    try:
        f()
    except:
        traceback.print_exc()
    sys.stdout = oldout
    sys.stderr = olderr
    res =  out.getvalue()
    out.close()
    return res

def character_info():
    import sys
    def task():
        oldargv = sys.argv
        sys.argv = [__name__, "-i", "-v", "/input.sav"]
        import ttwlsave.cli_info
        ttwlsave.cli_info.main()
        sys.argv = oldargv
    #return task()
    return wrap_io(task)

#  josephernest  https://github.com/pyodide/pyodide/issues/679#issuecomment-637519913
def load_file_from_browser():
    ''' saves the browser content as input_filename '''
    from js import content
    with open(input_filename,"wb") as fd:
        return fd.write(content.to_bytes())

def get_input_file():
    return file_to_buffer(input_filename)

def get_output_file():
    return file_to_buffer(output_filename)

def file_to_buffer(filename):
    from js import Uint8Array
    with open(filename,"rb") as fd:
        chunk = fd.read()
        x = Uint8Array.new(range(len(chunk)))
        x.assign(chunk)
        return x
    
def randomize_guid():
    from ttwlsave.ttwlsave import TTWLSave    
    save = TTWLSave( input_filename )
    save.randomize_guid();
    save.save_to( input_filename )
    return save.get_savegame_guid()

def get_guid():
    return sav.get_savegame_guid()

# duped in cli_edit.py
def unfinish_missions():
    from ttwlsave.ttwlsave import TTWLSave    
    save = TTWLSave( input_filename )
    save.randomize_guid();
    # duped in cli_edit.py
    save.set_playthroughs_completed(0)
    save.clear_playthrough_data(0)
    # duped in cli_edit.py
    save.save_to( input_filename )
    return save.get_savegame_guid()

def fake_tvhm():
    from ttwlsave.ttwlsave import TTWLSave    
    save = TTWLSave( input_filename )
    save.randomize_guid();
    # duped in cli_edit.py
    for missions in save.get_pt_completed_mission_lists():
        for mission in missions:
            if mission != "/Game/Missions/Plot/Mission_Plot11.Mission_Plot11_C":
                save.delete_mission(0,mission,allow_plot=True)
    save.set_playthroughs_completed(1)
    save.finish_game()
    # duped in cli_edit.py
    save.save_to( input_filename )
    return save.get_savegame_guid()

def import_items(items_text):
    filename = "/import.csv"
    with open(filename,"wt") as fd:
        fd.write(items_text)
    from ttwlsave.ttwlsave import TTWLSave    
    save = TTWLSave( input_filename )
    save.randomize_guid();
    guid = save.get_savegame_guid()
    import ttwlsave.cli_common
    def task():
        ttwlsave.cli_common.import_items(filename,
                                         save.create_new_item_encoded,
                                         save.add_item,
                                         file_csv=True,
                                         allow_fabricator=True,
                                         quiet=False
        )
    res =  wrap_io(task)
    save.save_to( input_filename )
    return to_js([res,guid])
