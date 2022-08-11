print("Booting Up Python")
import builtins
import micropip
from pyodide import to_js

sav = None
input_filename = "/input.sav"
output_filename = "/output.sav"
profile_filename = "/profile.sav"

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
    # await save_binary_url("https://softwareprocess.es/2022/example-ttwl.sav",input_filename)
    await save_binary_url("./example-ttwl.sav",input_filename)
    sav = TTWLSave("/input.sav")
    print(sav.get_char_name())
    return sav.get_char_name()

async def load_profile_example():
    global sav
    import ttwlsave
    from ttwlsave.ttwlsave import TTWLSave    
    await save_binary_url("./example-profile.sav",profile_filename)
    return profile_filename

def wrap_io(f):
    import io
    import sys
    out = io.StringIO()
    oldout = sys.stdout
    olderr = sys.stderr
    sys.stdout = sys.stderr = out
    try:
        f()
    except Exception as e:
        print(e)
        # traceback.print_exc()
    except SystemExit as e:
        print(e)
    sys.stdout = oldout
    sys.stderr = olderr
    res =  out.getvalue()
    out.close()
    return res

def character_info():
    import sys
    import ttwlsave.cli_info
    return call_commandline(
        ttwlsave.cli_info.main,
        [ "-i", "-v", input_filename ]
    )

def profile_info():
    import sys
    import ttwlsave.cli_prof_info
    return call_commandline(
        ttwlsave.cli_prof_info.main,
        [ "-i", "-v", "--rerolls", profile_filename ]
    )


#  josephernest  https://github.com/pyodide/pyodide/issues/679#issuecomment-637519913
def load_file_from_browser(filename=input_filename):
    ''' saves the browser content as input_filename '''
    from js import content
    with open(filename,"wb") as fd:
        return fd.write(content.to_bytes())

def get_input_file():
    return file_to_buffer(input_filename)

def get_profile_file():
    return file_to_buffer(profile_filename)

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
    from ttwlsave.ttwlsave import TTWLSave    
    save = TTWLSave( input_filename )
    return save.get_savegame_guid()

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

def item_types(item_type):
    from ttwlsave.ttwlsave import TTWLSave    
    save = TTWLSave( input_filename )
    save.randomize_guid();
    import ttwlsave.cli_common
    ttwlsave.cli_common.update_chaos_level(save.get_items(),
                    item_type,
                    False
    )
    save.save_to( input_filename )
    return save.get_savegame_guid()

def chaotic():
    return item_types(1)
def volatile():
    return item_types(2)
def primordial():
    return item_types(3)

def write_text(filename, items_text):
    with open(filename,"wt") as fd:
        fd.write(items_text)

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
                                         quiet=False
        )
    res =  wrap_io(task)
    save.save_to( input_filename )
    return to_js([res,guid])


def save_edit_command_line(args):
    args = args.to_py()
    import ttwlsave.cli_edit
    total_args = args + [input_filename, input_filename]
    print(total_args)
    return call_commandline(
        ttwlsave.cli_edit.main,
        total_args
    )

def profile_edit_command_line(args):
    args = args.to_py()
    import ttwlsave.cli_prof_edit
    return call_commandline(ttwlsave.cli_prof_edit.main,
                     args + [profile_filename, profile_filename])

def profile_info():
    import ttwlsave.cli_prof_info
    return call_commandline(ttwlsave.cli_prof_info.main, ["-i", "-v", profile_filename])

def call_commandline(our_main, args):
    import sys
    def task():
        oldargv = sys.argv
        sys.argv = [__name__] + args
        our_main()
        sys.argv = oldargv
    return wrap_io(task)
    
