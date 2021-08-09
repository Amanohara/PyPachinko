import glob
import os


def is_valid_args(arg1: str, arg2: str) -> bool:
    """引数validator.

    :param str arg1: 引数1(機種名)
    :param str arg2: 引数2(試行回数)
    :return: result (OK -> True, NG -> False)
    :rtype: bool
    """
    # 型チェック.
    try:
        machine_name = str(arg1)
        trials = int(arg2)
    except Exception as e:
        print(e)
        print('invalid parameter type')

        return False

    # machine/ 配下のファイル名一覧を取得.
    machines = [os.path.split(path)[1].removesuffix('.py') for path in glob.glob("machine/*.py")]

    # 存在しないmachine名の場合はエラー
    if f'{machine_name}' not in machines:
        print(f'machine name: {arg1} is invalid (not found)')
        print(f'machine modules that exist: {machines}')

        return False

    print('validation ok')

    return True
