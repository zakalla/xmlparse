#include "AutoParseConfig.h"

AutoParseConfig::AutoParseConfig()
{
}

AutoParseConfig::~AutoParseConfig()
{
}

bool AutoParseConfig::loadConfig()
{
  if (loadTransferFight() == false) return false;
  return true;
}

void AutoParseConfig::parseNodes(const XMLElement* root, std::string path, const std::string& rootname)
{
  if (root == nullptr) return;
  if (std::strcmp(root->Name(), "map") != 0 && std::strcmp(root->Name(), "vector") != 0 && root->RealNoChildren() == false)
  {
    path += root->Name();
    path += "_";
    for (const XMLElement* child = root->FirstChildElement(); child != nullptr; child = child->NextSiblingElement())
    {
      parseNodes(child, path, rootname);
    }
  }
  else
  {
    if (root->RealNoChildren() == true)
      path += root->Name();
    else
      path += root->Attribute("name");

    if (rootname.empty() == true)
      return;
    else if ("TransferFight" == rootname)
      funcTransferFight(root, path);
  }
}
