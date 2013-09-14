from __future__ import absolute_import

import gzip, mimetypes
from xml.dom import minidom

class dumper(object):
    def __init__(self, path):
        (mimetype, encoding) = mimetypes.guess_type(path)

        if mimetype == 'application/xml':
            if encoding == None:
                self._doc = minidom.parse(path)
            elif encoding == 'gzip':
                fh = gzip.open(path)
                self._doc = minidom.parse(fh)
                fh.close()
        else:
            raise Exception('Not an xml file.')
        self._dumper()

    def _dumper(self):
        stack = [ self._doc.documentElement ]

        while stack:
            cur = stack.pop()

            if cur:
                self._node_print(cur, len(stack))

                # Push the next sibling of the current node onto the stack
                # first so that it is the next node we visit after traversing
                # all its children. If there is no next sibling, we still need
                # to push a 'None' value onto the stack so that we can get the
                # proper depth of the children of the current node (which is
                # the last child node of its parent).
                stack.append(cur.nextSibling)
                # If the current node has children, push its first child onto
                # the stack so that it is the next node we visit after the
                # current iteration.
                if cur.childNodes:
                    stack.append(cur.firstChild)

    @staticmethod
    def _node_print(x, depth):
        if x.nodeName == '#text':
            s = x.nodeValue.strip().encode('utf-8')
            if s:
                print '    ' * depth, x.nodeName, ':', s,
        else:
            print '    ' * depth, '[', x.nodeName.upper(), ']',
            for i in range(x.attributes.length):
                print ':', x.attributes.item(i).name, '(', x.attributes.item(i).value.encode('utf-8'), ')',
        print

