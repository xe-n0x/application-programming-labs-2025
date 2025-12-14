import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt
from PIL import Image


def parsing() ->  argparse.Namespace:
     """Парсер"""
     parser = argparse.ArgumentParser()
     parser.add_argument('--input', type=str, required=True)
     parser.add_argument('--output', type=str, required=True)
     parser.add_argument('--min_val', type=int, required=True)
     parser.add_argument('--max_val', type=int, required=True)
     return  parser.parse_args()

def create_df(input: str, output: str) -> pd.DataFrame:
     '''создание Data Frame'''
     if not os.path.exists(input):
          raise FileNotFoundError(f"Файл {input} не найден.")
     df = pd.read_csv(input, header=0, names=['absolute path', 'relative path'])
     df.to_csv(output, index=False, encoding='utf-8')
     return df

def input_height(df: pd.DataFrame) -> None:
     '''добавление длины'''
     heights = []
     for i in range (len(df)):
          path = df.iloc[i]['absolute path']
          height = 0
          try:
               if os.path.exists(path):
                    with Image.open(path) as img:
                         height = img.height
          except:
               print(f"Изображение {path} не найдено.\n")
          heights.append(height)
     df['height'] = heights

def sort_by_height(df: pd.DataFrame, type: bool) -> pd.DataFrame: 
     '''type - тип сортировки: True - по возрастанию, False - по убыванию.'''
     '''Сортировка по ширине''' 
     return df.sort_values(by='height', ascending=type).reset_index(drop = True)

def filtered_by_height(df: pd.DataFrame, min: int, max: int) -> pd.DataFrame:
     '''Фильтрация по длине'''
     return df[(df['height'] >= min) & (df['height'] <= max)].reset_index(drop = True)

def graph(df: pd.DataFrame, output: str) -> None:
     '''График'''
     plt.plot(df['height'], color='black', marker='o', markersize=5)
     plt.title('Распределение длины по индексам')
     plt.xlabel('Индекс')
     plt.ylabel('Длина изображения')
     plt.xticks(range(len(df)))
     plt.grid()
     plt.savefig(output)
     plt.close()

def main() ->None:
     args = parsing()
     df = create_df(args.input, args.output)
     input_height(df)
     df.to_csv(args.output, index=False, encoding='utf-8')
     df_sorted = sort_by_height(df, True)
     df_sorted.to_csv("sorted.csv", index=False, encoding='utf-8')
     df_filtered = filtered_by_height(df_sorted, args.min_val, args.max_val)
     df_filtered.to_csv("filterred.csv", index = False, encoding='utf-8')
     graph(df_sorted, 'height_plot.png')

if __name__ == '__main__':
     main()