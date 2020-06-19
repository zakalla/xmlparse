#include "AutoParseConfig.h"

bool AutoParseConfig::loadTransferFight()
{
  XMLDocument doc;
  doc.LoadFile("/home/zyb/test/auto/config/TransferFight.xml");
  if (doc.ErrorID() != XML_SUCCESS) return false;
  if (doc.RootElement() == nullptr) return false;
  parseNodes(doc.RootElement(), "", doc.RootElement()->Name());
  return true;
}

void AutoParseConfig::funcTransferFight(const XMLElement* root, const std::string& path)
{
  if (path.empty() == true)
    return;
  else if ("TransferFight_ShowHints" == path)
    funcTransferFight_ShowHints(root);
  else if ("TransferFight_ItemScores" == path)
    funcTransferFight_ItemScores(root);
  else if ("TransferFight_LastTime" == path)
    funcTransferFight_LastTime(root);
  else if ("TransferFight_Reward" == path)
    funcTransferFight_Reward(root);
  else if ("TransferFight_Items" == path)
    funcTransferFight_Items(root);
  else if ("TransferFight_Sorts" == path)
    funcTransferFight_Sorts(root);
  else if ("TransferFight_SecondTransfer_LastTime" == path)
    funcTransferFight_SecondTransfer_LastTime(root);
  else if ("TransferFight_SecondTransfer_tt" == path)
    funcTransferFight_SecondTransfer_tt(root);
}

void AutoParseConfig::funcTransferFight_ShowHints(const XMLElement* element)
{
  if (element == nullptr) return;
  _TransferFight.ShowHints.clear();
  const char* key = element->Attribute("key");
  for (const XMLElement* child = element->FirstChildElement(); child != nullptr; child = child->NextSiblingElement())
  {
    if (child == nullptr || child->FirstAttribute() == nullptr || child->FirstAttribute()->Next() == nullptr || std::strcmp(child->FirstAttribute()->Name(), key) != 0)
      continue;
    TransferFight_ShowHints& p = _TransferFight.ShowHints[child->Attribute(key)];
    if (child->FindAttribute("value") != nullptr)
      p.value = child->Attribute("value");
  }
}

void AutoParseConfig::funcTransferFight_ItemScores(const XMLElement* element)
{
  if (element == nullptr) return;
  _TransferFight.ItemScores.clear();
  for (const XMLElement* child = element->FirstChildElement(); child != nullptr; child = child->NextSiblingElement())
  {
    if (child == nullptr || child->FirstAttribute() == nullptr || child->FirstAttribute()->Next() == nullptr)
      continue;
    TransferFight_ItemScores data;
    if (child->FindAttribute("id") != nullptr)
      data.id = child->Attribute("id");
    if (child->FindAttribute("score") != nullptr)
      data.score = child->Attribute("score");
    _TransferFight.ItemScores.push_back(data);
  }
}

void AutoParseConfig::funcTransferFight_LastTime(const XMLElement* element)
{
  if (element == nullptr || element->FirstChild() == nullptr) return;
  _TransferFight.LastTime = element->FirstChild()->Value();
}

void AutoParseConfig::funcTransferFight_Reward(const XMLElement* element)
{
  if (element == nullptr || element->FirstAttribute() == nullptr) return;
  if (element->FindAttribute("itemid") != nullptr)
    _TransferFight.Reward.itemid = element->Attribute("itemid");
  if (element->FindAttribute("itemnum") != nullptr)
    _TransferFight.Reward.itemnum = element->Attribute("itemnum");
}

void AutoParseConfig::funcTransferFight_Items(const XMLElement* element)
{
  if (element == nullptr || element->FirstChild() == nullptr) return;
  _TransferFight.Items = element->FirstChild()->Value();
}

void AutoParseConfig::funcTransferFight_Sorts(const XMLElement* element)
{
  if (element == nullptr || element->FirstChild() == nullptr) return;
  _TransferFight.Sorts = element->FirstChild()->Value();
}

void AutoParseConfig::funcTransferFight_SecondTransfer_LastTime(const XMLElement* element)
{
  if (element == nullptr || element->FirstChild() == nullptr) return;
  _TransferFight._TransferFight_SecondTransfer.LastTime = element->FirstChild()->Value();
}

void AutoParseConfig::funcTransferFight_SecondTransfer_tt(const XMLElement* element)
{
  if (element == nullptr || element->FirstChild() == nullptr) return;
  _TransferFight._TransferFight_SecondTransfer.tt = element->FirstChild()->Value();
}

