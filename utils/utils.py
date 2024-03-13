import omitempty

class Serializer(object):
  """
  連続したデータを整形するためのクラス
  talibでの解析に使用するデータを整形する
  """
  @property
  def value(self):
    dict_value =omitempty(self.__dict__)
    if not dict_value:
      return None
    
    return self.__dict__
