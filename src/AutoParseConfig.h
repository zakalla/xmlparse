#pragma once

#include "tinyxml2.h"
#include "singleton.h"
#include "TransferFight.h"

using namespace std;
using namespace tinyxml2;
using namespace Prs;

class AutoParseConfig : public singleton<AutoParseConfig>
{
  friend class singleton<AutoParseConfig>;
  public:
    AutoParseConfig();
    ~AutoParseConfig();
    bool loadConfig();
  private:
    void parseNodes(const XMLElement* root, std::string path, const std::string& rootname);

  private:
    TransferFight _TransferFight;
  public:
    const TransferFight& getTransferFight() const { return _TransferFight; }
  private:
    bool loadTransferFight();
    void funcTransferFight(const XMLElement* root, const std::string& path);
    void funcTransferFight_ShowHints(const XMLElement* element);
    void funcTransferFight_ItemScores(const XMLElement* element);
    void funcTransferFight_LastTime(const XMLElement* element);
    void funcTransferFight_Reward(const XMLElement* element);
    void funcTransferFight_Items(const XMLElement* element);
    void funcTransferFight_Sorts(const XMLElement* element);
    void funcTransferFight_SecondTransfer_LastTime(const XMLElement* element);
    void funcTransferFight_SecondTransfer_tt(const XMLElement* element);
};
