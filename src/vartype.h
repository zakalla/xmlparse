#pragma once

#include <string>
#include <vector>
#include <set>
#include <map>
#include <iostream>

unsigned long stringTok(std::string s, std::string k, std::vector<std::string> &v);

class VarType
{
  friend std::ostream & operator << (std::ostream& out, const VarType& val);
  public:
    VarType()
    {
    }

    VarType(const VarType& val)
    {
      this->m_str = val.m_str;
    }

    VarType& operator = (const VarType& var)
    {
      if (&var != this)
      {
        this->m_str.clear();
        this->m_str = var.m_str;
      }
      return *this;
    }

    bool operator < (const VarType& var) const
    {
      if (this->m_str < var.m_str)
      {
        return true;
      }
      return false;
    }

    bool operator > (const VarType& var) const
    {
      if (this->m_str > var.m_str)
      {
        return true;
      }
      return false;
    }

    bool operator == (const VarType& var) const
    {
      if (this->m_str == var.m_str)
      {
        return true;
      }
      return false;
    }

    bool operator <= (const VarType& var) const
    {
      if (this->m_str <= var.m_str)
      {
        return true;
      }
      return false;
    }

    bool operator >= (const VarType& var) const
    {
      if (this->m_str >= var.m_str)
      {
        return true;
      }
      return false;
    }

    bool operator != (const VarType& var) const
    {
      if (this->m_str != var.m_str)
      {
        return true;
      }
      return false;
    }

    VarType(const std::string& val)
    {
      m_str = val;
    }

    VarType(const char* val)
    {
      m_str = val;
    }

    VarType(int val)
    {
      m_str = std::to_string(val);
    }

    VarType(unsigned int val)
    {
      m_str = std::to_string(val);
    }

    VarType(long val)
    {
      m_str = std::to_string(val);
    }

    VarType(unsigned long val)
    {
      m_str = std::to_string(val);
    }

    VarType(float var)
    {
      m_str = std::to_string(var);
    }

    VarType(double var)
    {
      m_str = std::to_string(var);
    }

    operator const char* () const
    {
      return m_str.c_str();
    }

    operator int () const
    {
      if (m_str.empty()) return 0;
      return std::stoi(m_str);
    }

    operator unsigned int () const
    {
      if (m_str.empty()) return 0;
      return static_cast<unsigned int>(std::stoul(m_str));
    }

    operator long () const
    {
      if (m_str.empty()) return 0;
      return std::stol(m_str);
    }

    operator unsigned long () const
    {
      if (m_str.empty()) return 0;
      return std::stoul(m_str);
    }

    operator float () const
    {
      if (m_str.empty()) return 0;
      return std::stof(m_str);
    }

    operator double () const
    {
      if (m_str.empty()) return 0;
      return std::stod(m_str);
    }

    template <typename T>
    operator std::vector<T> () const
    {
      std::vector<std::string> sv;
      stringTok(m_str, ":", sv);
      std::vector<T> vec;
      for(unsigned long n = 0; n < sv.size(); ++n)
      {
        VarType value1 = sv[n];
        T value2(value1);
        vec.push_back(value2);
      }
      return vec;
    }

    template <typename T>
    operator std::set<T> () const
    {
      std::vector<std::string> sv;
      stringTok(m_str, ":", sv);
      std::set<T> sst;
      for(unsigned long n = 0; n < sv.size(); ++n)
      {
        VarType value1 = sv[n];
        T value2(value1);
        sst.insert(value2);
      }
      return sst;
    }

    template <typename T1, typename T2>
    operator std::map<T1, T2> () const
    {
      std::vector<std::string> sv;
      stringTok(m_str, ":", sv);
      std::map<T1, T2> mpp;
      for (unsigned long n = 0; n < sv.size(); ++n)
      {
        std::string::size_type i = sv[n].find_first_not_of("|", 0);
        if (i == std::string::npos)
        {
          continue;
        }
        std::string::size_type j = sv[n].find_first_of("|", i);
        if (j == std::string::npos || j+1 == std::string::npos)
        {
          continue;
        }
        VarType value1 = sv[n].substr(i, j-i);
        VarType value2 = sv[n].substr(j+1, sv[n].length()-j-1);
        T1 value3(value1);
        T2 value4(value2);
        mpp.emplace(value3, value4);
      }
      return mpp;
    }
  private:
    std::string m_str;
};
