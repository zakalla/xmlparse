#pragma once

template <typename T>
class singleton
{
  private:
    singleton(const singleton &);
    const singleton &operator=(const singleton &);

  protected:
    static T *_instance;
    singleton(){
    }
    virtual ~singleton(){}

  public:
    static void delMe()
    {
      if (!_instance)
      {
        delete(_instance);
        _instance = nullptr;
      }
    }
    static T* instance()
    {
      if (!_instance)
        _instance = new T;
      return _instance;
    }
    static T& getMe()
    {
      if (!_instance)
        _instance = new T;
      return *_instance;
    }
    static void setInstance(T* t)
    {
      _instance = t;
    }
};

template <typename T>
T* singleton<T>::_instance = 0;
