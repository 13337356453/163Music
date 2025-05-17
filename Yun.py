import argparse
import os
import ast
from Musicer import Musicer
from Searcher import Searcher


def banner():
    print("=" * 60)
    print("🎵  欢迎使用".center(60))
    print("网易云音乐下载器".center(60))
    print("-" * 60)
    print("Author : manlu".ljust(40) + "Time : 2025.5")
    print("GitHub : https://github.com/13337356453/163Music")
    print("=" * 60)
    print("使用方法: python script.py -k <关键词或文件> -c <Cookie> [其他选项]")
    print("使用 -h 参数查看更多说明")
    print()
def parse_args():
    if_file=False
    parser = argparse.ArgumentParser(
        description='网易云音乐下载器 - 控制台参数说明',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-k', '--keywords', type=str, required=True,
                        help='关键词字符串或关键词文件名（文件必须存在且非空）')
    parser.add_argument('-n', '--number', type=int, default=1,
                        help='下载数量，正整数，默认1，不能大于30')
    parser.add_argument('-c', '--cookie', type=str, required=True,
                        help='Cookie信息，必须提供')
    parser.add_argument('-p', '--proxy', type=str, default='',
                        help='代理信息，格式为Python字典字符串')
    parser.add_argument('-o', '--output', type=str, default='./music',
                        help='输出目录，默认 ./music')

    args = parser.parse_args()
    args.keywords=args.keywords.strip()
    if os.path.isfile(args.keywords):
        if_file=True
        if os.path.getsize(args.keywords) == 0:
            parser.error(f"[!] 关键词文件 '{args.keywords}' 为空")
    elif args.keywords.strip() == '':
        parser.error("[!] 关键词字符串不能为空")

    if args.number <= 0:
        parser.error("[!] 参数 -n/--number 必须为正整数")
    if args.number > 30:
        parser.error("[!] 参数 -n/--number 必须小于等于30")
    if args.proxy:
        try:
            proxy_dict = ast.literal_eval(args.proxy)
            if not isinstance(proxy_dict, dict):
                raise ValueError
        except Exception:
            parser.error("[!] 参数 -p/--proxy 必须为合法的字典字符串")

    return args,if_file
def main():
    banner()
    args,if_file = parse_args()
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    kws=[]
    if if_file:
        f=open(args.keywords,'r',encoding='utf-8')
        kws=[x.strip() for x in f.readlines() if x.strip()!=""]
        f.close()
    else:
        kws.append(args.keywords)
    for kw in kws:
        searcher=Searcher(keyword=kw,cookie=args.cookie,number=args.number,proxies=args.proxy)
        datas=searcher.getData()
        if datas==None:
            print(f"[-] 关键字[{kw}]获取数据失败")
            continue
        for data in datas:
            singer=data['ar'][0]['name']
            name=data['name']
            musicid=data['id']
            musicer=Musicer(musicid=musicid,cookie=args.cookie,name=f'{args.output}/{name}-{singer}',proxies=args.proxy)
            musicer.download()
            del musicer
        del searcher
if __name__ == '__main__':
    main()