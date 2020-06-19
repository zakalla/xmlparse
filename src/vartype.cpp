#include "vartype.h"

unsigned long stringTok(std::string s, std::string k, std::vector<std::string> &v)
{
  std::string::size_type len = s.length();
  std::string::size_type i = 0, j = 0;

  while (i<len)
  {
    i = s.find_first_not_of(k, i);
    if (i==std::string::npos) break;

    j = s.find_first_of(k, i);
    if (j==std::string::npos)
    {
      v.push_back(s.substr(i, len-i));
      break;
    }
    else
    {
      v.push_back(s.substr(i, j-i));
      i = j+1;
    }
  }
  return v.size();
}

std::ostream & operator << (std::ostream& out, const VarType& val)
{
  out << val.m_str;
  return out;
}
