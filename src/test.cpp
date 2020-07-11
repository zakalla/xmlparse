#include "AutoParseConfig.h"

int main()
{
  if (AutoParseConfig::getMe().loadConfig() == false)
  {
    return 0;
  }

  auto& rCFG = AutoParseConfig::getMe().getTransferFight();

  std::cout << "第一种配置格式解析:" << std::endl;
  auto& mapShowHints = rCFG.ShowHints;
  for (auto& m : mapShowHints)
  {
    std::cout << m.first << ' ' << m.second.value << std::endl;
  }

  std::cout << "第二种配置格式解析:" << std::endl;
  auto& vecItemScores = rCFG.ItemScores;
  for (auto& v : vecItemScores)
  {
    std::cout << v.id << ' ' << v.score << std::endl;
  }

  std::cout << "第三种配置格式解析:" << std::endl;
  int lastTime = rCFG.LastTime;
  std::cout << lastTime << std::endl;

  std::cout << "第四种配置格式解析:" << std::endl;
  auto rwd = rCFG.Reward;
  std::cout << int(rwd.itemid) << ' ' << int(rwd.itemnum) << std::endl;

  std::cout << "第五种配置格式解析(1):" << std::endl;
  const std::vector<int>& vc = rCFG.Items;
  for (auto& v : vc)
  {
    std::cout << v << ' ';
  }
  std::cout << std::endl;

  std::cout << "第五种配置格式解析(2):" << std::endl;
  const std::set<int>& st = rCFG.Items;
  for (auto& s : st)
  {
    std::cout << s << ' ';
  }
  std::cout << std::endl;

  std::cout << "第六种配置格式解析:" << std::endl;
  const std::map<int, std::string>& mp = rCFG.Sorts;
  for (auto& m : mp)
  {
    std::cout << m.first << ' ' << m.second << std::endl;
  }

  std::cout << "多层配置格式解析:" << std::endl;
  int lastTime2 = rCFG.getSecondTransfer().LastTime;
  std::cout << lastTime2 << std::endl;

  return 0;
}
