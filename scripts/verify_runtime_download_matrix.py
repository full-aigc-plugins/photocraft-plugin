"""Fixed installed downloader: transient retries and final local/HTTP failures."""
import argparse, errno, hashlib, http.client, importlib.util, json, ssl, tempfile
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

def verify(skill):
    source=skill/'scripts/bootstrap.py'; spec=importlib.util.spec_from_file_location('fixed_download_matrix',source); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    url=json.loads(source.with_name('runtime.lock.json').read_text())['artifacts']['darwin-arm64']['url']; rows=[]
    class Response:
        url='https://objects.githubusercontent.com/fixture'
        headers={'Content-Length':'8'}
        def __init__(self):self.data=b'complete'
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def read(self,size):data,self.data=self.data,b'';return data
    transient=[('timeout',TimeoutError()),('connection',ConnectionResetError()),('ssl-eof',ssl.SSLEOFError()),('wrapped-timeout',URLError(TimeoutError())),('short-read',http.client.IncompleteRead(b'half',4))]
    transient += [('http-'+str(code),HTTPError(url,code,'fixture',{},None)) for code in [408,429,500,503,599]]
    final=[('certificate',ssl.SSLCertVerificationError()),('wrapped-certificate',URLError(ssl.SSLCertVerificationError())),('permission',PermissionError(errno.EACCES,'fixture')),('disk-full',OSError(errno.ENOSPC,'fixture'))]
    final += [('http-'+str(code),HTTPError(url,code,'fixture',{},None)) for code in [400,401,403,404,409,422,600]]
    with tempfile.TemporaryDirectory() as temporary:
        target=Path(temporary)/'archive.zip'
        for name,error in transient:
            target.write_bytes(b'old-partial')
            with patch.object(module.urllib.request,'urlopen',side_effect=[error,Response()]) as fetch,patch.object(module.time,'sleep'):
                module.download(url,target);assert fetch.call_count==2;assert target.read_bytes()==b'complete'
            rows.append({'class':name,'expectedAttempts':2,'actualAttempts':2,'partialReplaced':True,'result':'PASS'})
        for name,error in final:
            target.unlink(missing_ok=True)
            with patch.object(module.urllib.request,'urlopen',side_effect=error) as fetch,patch.object(module.time,'sleep'):
                try:module.download(url,target)
                except type(error):pass
                else:raise AssertionError(name+' was accepted')
                assert fetch.call_count==1,(name,fetch.call_count)
            rows.append({'class':name,'expectedAttempts':1,'actualAttempts':1,'result':'PASS'})
        with patch.object(module.urllib.request,'urlopen',side_effect=TimeoutError()) as fetch,patch.object(module.time,'sleep'):
            try:module.download(url,target)
            except ValueError as error:assert 'three read-only attempts' in str(error)
            else:raise AssertionError('retry exhaustion accepted')
            assert fetch.call_count==3 and not target.exists()
        rows.append({'class':'retry-exhaustion','actualAttempts':3,'partialDiscarded':True,'result':'PASS'})
    return {'schema':'photocraft-download-boundary-matrix/v1','status':'PASS','bootstrapSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':rows,'scope':'Actual fixed installed Python module with mocked transport faults; live public cold-download proof recorded separately; integrity/extraction/install checks covered by fixed-bootstrap15','nativeEdits':0}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--skill-root',type=Path,required=True);parser.add_argument('--evidence',type=Path,required=True);args=parser.parse_args();proof=verify(args.skill_root);proof['driverSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();args.evidence.write_text(json.dumps(proof,indent=2)+'\n');print(str(len(proof['cases']))+' download boundaries: PASS')
