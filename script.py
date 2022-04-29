print("Booting Up Python")
import builtins
import micropip

sav = None
input_filename = "/input.sav"
output_filename = "/output.sav"

async def install_deps():
    await micropip.install('setuptools')
    import setuptools
    await micropip.install('https://softwareprocess.es/2022/ttwl_cli_saveedit-0.0.3-py3-none-any.whl')
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
