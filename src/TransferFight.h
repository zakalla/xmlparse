#pragma once

#include "vartype.h"

namespace Prs
{
  struct TransferFight_ShowHints
  {
    VarType value;
  };

  struct TransferFight_ItemScores
  {
    VarType id;
    VarType score;
  };

  struct TransferFight_Reward
  {
    VarType itemid;
    VarType itemnum;
  };

  struct TransferFight_SecondTransfer
  {
    VarType LastTime;
    VarType tt;
  };

  struct TransferFight
  {
    VarType LastTime;
    VarType Items;
    VarType Sorts;
    TransferFight_Reward Reward;
    std::map<VarType, TransferFight_ShowHints> ShowHints;
    std::vector<TransferFight_ItemScores> ItemScores;
    TransferFight_SecondTransfer _TransferFight_SecondTransfer;
    const TransferFight_SecondTransfer& getSecondTransfer() const { return _TransferFight_SecondTransfer; }
  };
}