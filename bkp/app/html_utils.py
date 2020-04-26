
import ure
from html.entities import name2codepoint as n2cp

def unescape(string):
    def subst_entity(match):
        ent = match.group(2)
        if match.group(1) == '#':
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)
            if cp:
                return unichr(cp)
            else:
                return match.group()
    enity_re = ure.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(subst_entity, string)[0]

