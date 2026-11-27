"""Read complete stock smoke verdicts; partial positives are never coverage."""
import re
def qualify_log(raw,viewport,stage):
    plain=re.sub(r'\x1b\[[0-9;]*m','',raw)
    text='\n'.join(re.sub(r'^.*?\d{4}-\d\d-\d\dT[\d:.]+Z\s','',line) for line in plain.splitlines())
    assert re.search(r'^serving .* — PUBLISHED mirror',text,re.M),'Published mirror not identified'
    assert f'NOT THE FULL GATE — viewports filtered to "{viewport}"' in text,'Wrong viewport'
    assert f'NOT THE FULL GATE — stages filtered to "{stage}"' in text,'Wrong stages'
    label={'desktop':'desktop 1280x800','mobile':'mobile 390x780'}[viewport]
    actual=re.findall(r'^(mobile 390x780|desktop 1280x800):\s*$',text,re.M)
    assert actual==[label],('Unexpected viewport sections',actual)
    assert not re.search(r'^\s{2}FAIL\s',text,re.M),'A smoke assertion failed'
    assert re.search(r'^\s{2}pass\s+(?:\[\d+:\d\d\]\s+)?'+re.escape(label)+r': zero page errors\b',text,re.M),'Missing final zero-page-error check'
    summaries=re.findall(r'^(\d+) passed, (\d+) failed\s*$',text,re.M)
    assert len(summaries)==1 and int(summaries[0][0])>0 and int(summaries[0][1])==0,('No complete success footer',summaries)
    return {'viewport':viewport,'stage':stage,'passed_assertions':int(summaries[0][0]),'failed_assertions':0,'zero_page_errors':True,'published':True,'whole_requested_body_complete':True}
