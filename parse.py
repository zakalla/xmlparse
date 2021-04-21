try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import os
import sys
import collections

space = ' '

def noChild(root):
  for child in root:
    return False
  return True

def parseNodes(root, path, node, dicc, lines, line2, line3, lineAll1):
  if root.tag == 'vector':
    if noChild(root):
      return
    if 'name' not in root.attrib:
      return
    path = path + root.attrib['name']
    dicc['vec'].append(path)
    dicc['vec'].append(root.attrib['name'])
    lineAll1.append(4*space + 'void func{path}(const XMLElement* element);\n'.format(path=path))
    line2.append(2*space + 'else if (\"{path}\" == path)\n'.format(path=path))
    line2.append(4*space + 'func{path}(root);\n'.format(path=path))
    line3.append('void AutoParseConfig::func{path}(const XMLElement* element)\n'.format(path=path) + '{\n')
    line3.append(2*space + 'if (element == nullptr) return;\n')
    variable = ''
    for n in node:
      variable = variable + n + '.'
    variable = variable + root.attrib['name']
    line3.append(2*space + '{variable}.clear();\n'.format(variable=variable))
    line3.append(2*space + 'for (const XMLElement* child = element->FirstChildElement(); child != nullptr; child = child->NextSiblingElement())\n' + 2*space + '{\n')
    line3.append(4*space + 'if (child == nullptr || child->FirstAttribute() == nullptr || child->FirstAttribute()->Next() == nullptr)\n')
    line3.append(6*space + 'continue;\n')
    line3.append(4*space + '{path} data;\n'.format(path=path))
    lines.append('\n' + 2*space + 'struct {path}\n'.format(path=path) + 2*space + '{\n')
    sortAttr = sorted(root[0].attrib, key = lambda asd:asd[0])
    for k in sortAttr:
      line3.append(4*space + 'if (child->FindAttribute(\"{item}\") != nullptr)\n'.format(item=k))
      line3.append(6*space + 'data.{item} = child->Attribute(\"{item}\");\n'.format(item=k))
      lines.append(4*space + 'VarType {k};\n'.format(k=k))
    line3.append(4*space + '{variable}.push_back(data);\n'.format(variable=variable))
    line3.append(2*space + '}\n')
    line3.append('}' + 2*'\n')
    lines.append(2*space + '};\n')

  elif root.tag == 'map':
    if noChild(root) == True:
      return
    if 'name' not in root.attrib:
      return
    path = path + root.attrib['name']
    dicc['map'].append(path)
    dicc['map'].append(root.attrib['name'])
    lineAll1.append(4*space + 'void func{path}(const XMLElement* element);\n'.format(path=path))
    line2.append(2*space + 'else if (\"{path}\" == path)\n'.format(path=path))
    line2.append(4*space + 'func{path}(root);\n'.format(path=path))
    line3.append('void AutoParseConfig::func{path}(const XMLElement* element)\n'.format(path=path) + '{\n')
    line3.append(2*space + 'if (element == nullptr) return;\n')
    variable = ''
    for n in node:
      variable = variable + n + '.'
    variable = variable + root.attrib['name']
    line3.append(2*space + '{variable}.clear();\n'.format(variable=variable))
    line3.append(2*space + 'const char* key = element->Attribute("key");\n')
    line3.append(2*space + 'for (const XMLElement* child = element->FirstChildElement(); child != nullptr; child = child->NextSiblingElement())\n' + 2*space + '{\n')
    line3.append(4*space + 'if (child == nullptr || child->FirstAttribute() == nullptr || child->FirstAttribute()->Next() == nullptr || std::strcmp(child->FirstAttribute()->Name(), key) != 0)\n')
    line3.append(6*space + 'continue;\n')
    line3.append(4*space + '{path}& p = {variable}[child->Attribute(key)];\n'.format(path=path, variable=variable))
    lines.append('\n' + 2*space + 'struct {path}\n'.format(path=path) + 2*space + '{\n')
    sortAttr = sorted(root[0].attrib, key = lambda asd:asd[0])
    for k in sortAttr:
      if k != root.attrib['key']:
        line3.append(4*space + 'if (child->FindAttribute(\"{item}\") != nullptr)\n'.format(item=k))
        line3.append(6*space + 'p.{item} = child->Attribute(\"{item}\");\n'.format(item=k))
        lines.append(4*space + 'VarType {k};\n'.format(k=k))
    line3.append(2*space + '}\n')
    line3.append('}' + 2*'\n')
    lines.append(2*space + '};\n')

  elif noChild(root) == True:
    path += root.tag
    lineAll1.append(4*space + 'void func{path}(const XMLElement* element);\n'.format(path=path))
    line2.append(2*space + 'else if (\"{path}\" == path)\n'.format(path=path))
    line2.append(4*space + 'func{path}(root);\n'.format(path=path))
    if len(root.attrib) == 0:
      dicc['var'].append(path)
      dicc['var'].append(root.tag)
      line3.append('void AutoParseConfig::func{path}(const XMLElement* element)\n'.format(path=path) + '{\n')
      line3.append(2*space + 'if (element == nullptr || element->FirstChild() == nullptr) return;\n')
      variable = ''
      for n in node:
        variable = variable + n + '.'
      variable = variable + root.tag
      line3.append(2*space + '{variable} = element->FirstChild()->Value();\n'.format(variable=variable))
      line3.append('}' + 2*'\n')
    else:
      dicc['svar'].append(path)
      dicc['svar'].append(root.tag)
      lines.append('\n' + 2*space + 'struct {path}\n'.format(path=path) + 2*space + '{\n')
      line3.append('void AutoParseConfig::func{path}(const XMLElement* element)\n'.format(path=path) + '{\n')
      line3.append(2*space + 'if (element == nullptr || element->FirstAttribute() == nullptr) return;\n')
      variable = ''
      for n in node:
        variable = variable + n + '.'
      variable = variable + root.tag
      sortAttr = sorted(root.attrib, key = lambda asd:asd[0])
      for k in sortAttr:
        line3.append(2*space + 'if (element->FindAttribute(\"{item}\") != nullptr)\n'.format(item=k))
        line3.append(4*space + '{variable}.{item} = element->Attribute(\"{item}\");\n'.format(variable=variable, item=k))
        lines.append(4*space + 'VarType {k};\n'.format(k=k))
      line3.append('}' + 2*'\n')
      lines.append(2*space + '};\n')

  else:
    path = path + root.tag
    dicc['str'].append(path)
    dicc['str'].append('_' + path)
    dicc['str'].append(root.tag)
    di = collections.defaultdict(list)
    di['key'].append(path)
    nodes = node + ('_'+path,)
    path = path + '_'
    for child in root:
      parseNodes(child, path, nodes, di, lines, line2, line3, lineAll1)
    if  'key' not in di or len(di['key']) == 0:
      return
    lines.append('\n' + 2*space + 'struct {key}\n'.format(key=di['key'][0]) + 2*space + '{\n')
    if 'var' in di:
      next = 0
      while (next+1 < len(di['var'])):
        lines.append(4*space + 'VarType {value};\n'.format(value=di['var'][next+1]))
        next = next + 2
    if 'svar' in di:
      next = 0
      while (next+1 < len(di['svar'])):
        lines.append(4*space + '{name} {value};\n'.format(name=di['svar'][next], value=di['svar'][next+1]))
        next = next + 2
    if 'map' in di:
      next = 0
      while (next+1 < len(di['map'])):
        lines.append(4*space + 'std::map<VarType, {name}> {value};\n'.format(name=di['map'][next], value=di['map'][next+1]))
        next = next + 2
    if 'vec' in di:
      next = 0
      while (next+1 < len(di['vec'])):
        lines.append(4*space + 'std::vector<{name}> {value};\n'.format(name=di['vec'][next], value=di['vec'][next+1]))
        next = next + 2
    if 'str' in di:
      next = 0
      while (next+1 < len(di['str'])):
        lines.append(4*space + '{name} {value};\n'.format(name=di['str'][next], value=di['str'][next+1]))
        lines.append(4*space + 'const {name}& get{tag}() const {{ return {value}; }}\n'.format(name=di['str'][next], value=di['str'][next+1], tag = di['str'][next+2]))
        next = next + 3
    lines.append(2*space + '};\n')

def parseFiles(fileName, fileDir, srcDir, lineAll0, lineAll1, lineAll2, lineAll3):
  tree = ET.parse(fileDir + fileName)
  rootName = tree.getroot().tag
  if rootName + '.xml' != fileName:
    print ('rootName no equal fileName !')
    return False

  lineAll0.append('#include "{name}.h"\n'.format(name=rootName))
  lineAll1.append('\n' + 2*space + 'private:\n')
  lineAll1.append(4*space + '{name} _{name};\n'.format(name=rootName))
  lineAll1.append(2*space + 'public:\n')
  lineAll1.append(4*space + 'const {name}& get{name}() const {{ return _{name}; }}\n'.format(name=rootName))
  lineAll1.append(2*space + 'private:\n')
  lineAll1.append(4*space + 'bool load{name}();\n'.format(name=rootName))
  lineAll1.append(4*space + 'void func{name}(const XMLElement* root, const std::string& path);\n'.format(name=rootName))

  lineAll2.append(2*space + 'if (load{name}() == false) return false;\n'.format(name=rootName))
  lineAll3.append(4*space + 'else if ("{name}" == rootname)\n'.format(name=rootName))
  lineAll3.append(6*space + 'func{name}(root, path);\n'.format(name=rootName))

  lines = []
  lines.append('#pragma once' + 2*'\n')
  lines.append('#include "vartype.h"' + 2*'\n')
  lines.append('namespace Prs\n' + '{')

  line2 = []
  line2.append('#include "AutoParseConfig.h"' + 2*'\n')
  line2.append('bool AutoParseConfig::load{name}()\n'.format(name=rootName) + '{\n')
  line2.append(2*space + 'XMLDocument doc;\n')
  line2.append(2*space + 'doc.LoadFile("{dir}{name}");\n'.format(dir=fileDir, name=fileName))
  line2.append(2*space + 'if (doc.ErrorID() != XML_SUCCESS) return false;\n')
  line2.append(2*space + 'if (doc.RootElement() == nullptr) return false;\n')
  line2.append(2*space + 'parseNodes(doc.RootElement(), "", doc.RootElement()->Name());\n')
  line2.append(2*space + 'return true;\n}' + 2*'\n')
  line2.append('void AutoParseConfig::func{name}(const XMLElement* root, const std::string& path)\n'.format(name=rootName) + '{\n')
  line2.append(2*space + 'if (path.empty() == true)\n')
  line2.append(4*space + 'return;\n')

  line3 = []

  parseNodes(tree.getroot(), '', (), collections.defaultdict(list), lines, line2, line3, lineAll1)

  lines.append('}')
  filePath = srcDir + rootName + '.h'
  openFile = open(filePath, 'w')
  openFile.writelines(lines)
  openFile.close()

  line2.append('}' + 2*'\n')
  filePath = srcDir + rootName + '.cpp'
  openFile = open(filePath, 'w')
  openFile.writelines(line2)
  openFile.writelines(line3)
  openFile.close()

  print ('generator %s succeed !' % fileName)

  return True

def parseAll(fileDir, srcDir):
  lineAll2 = []
  lineAll2.append('#include "AutoParseConfig.h"' + 2*'\n')
  lineAll2.append('AutoParseConfig::AutoParseConfig()\n' + '{\n}' +2*'\n')
  lineAll2.append('AutoParseConfig::~AutoParseConfig()\n' + '{\n}' +2*'\n')
  lineAll2.append('bool AutoParseConfig::loadConfig()\n' + '{\n')

  lineAll3 = []
  lineAll3.append('void AutoParseConfig::parseNodes(const XMLElement* root, std::string path, const std::string& rootname)\n' + '{\n')
  lineAll3.append(2*space + 'if (root == nullptr) return;\n')
  lineAll3.append(2*space + 'if (std::strcmp(root->Name(), "map") != 0 && std::strcmp(root->Name(), "vector") != 0 && root->RealNoChildren() == false)\n' + 2*space + '{\n')
  lineAll3.append(4*space + 'path += root->Name();\n')
  lineAll3.append(4*space + 'path += "_";\n')
  lineAll3.append(4*space + 'for (const XMLElement* child = root->FirstChildElement(); child != nullptr; child = child->NextSiblingElement())\n' + 4*space + '{\n')
  lineAll3.append(6*space + 'parseNodes(child, path, rootname);\n' + 4*space + '}\n' + 2*space + '}\n')
  lineAll3.append(2*space + 'else\n' + 2*space + '{\n')
  lineAll3.append(4*space + 'if (root->RealNoChildren() == true)\n')
  lineAll3.append(6*space + 'path += root->Name();\n')
  lineAll3.append(4*space + 'else\n')
  lineAll3.append(6*space + 'path += root->Attribute("name");' + 2*'\n')
  lineAll3.append(4*space + 'if (rootname.empty() == true)\n')
  lineAll3.append(6*space + 'return;\n')

  lineAll0 = []
  lineAll0.append('#pragma once' + 2*'\n')
  lineAll0.append('#include "tinyxml2.h"\n')
  lineAll0.append('#include "singleton.h"\n')

  lineAll1 = []

  nameList = os.listdir(fileDir)
  for f in nameList:
    if f.endswith('.xml', 0, len(f)) == True and parseFiles(f, fileDir, srcDir, lineAll0, lineAll1, lineAll2, lineAll3) == False:
      print ('generator %s fail !' % f)
      return

  lineAll0.append('\n' + 'using namespace std;\n')
  lineAll0.append('using namespace tinyxml2;\n')
  lineAll0.append('using namespace Prs;' + 2*'\n')
  lineAll0.append('class AutoParseConfig : public singleton<AutoParseConfig>\n' + '{\n')
  lineAll0.append(2*space + 'friend class singleton<AutoParseConfig>;\n')
  lineAll0.append(2*space + 'public:\n')
  lineAll0.append(4*space + 'AutoParseConfig();\n')
  lineAll0.append(4*space + '~AutoParseConfig();\n')
  lineAll0.append(4*space + 'bool loadConfig();\n')
  lineAll0.append(2*space + 'private:\n')
  lineAll0.append(4*space + 'void parseNodes(const XMLElement* root, std::string path, const std::string& rootname);\n')
  lineAll1.append('};\n')

  filePath = srcDir + 'AutoParseConfig.h'
  openFile = open(filePath, 'w')
  openFile.writelines(lineAll0)
  openFile.writelines(lineAll1)

  lineAll2.append(2*space + 'return true;\n')
  lineAll2.append('}' + 2*'\n')
  lineAll3.append(2*space + '}\n' + '}\n')

  filePath = srcDir + 'AutoParseConfig.cpp'
  openFile = open(filePath, 'w')
  openFile.writelines(lineAll2)
  openFile.writelines(lineAll3)
  openFile.close()

  print('Complete !')

parseAll(sys.path[0]+'/config/', sys.path[0]+'/src/')
