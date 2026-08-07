"""
QPhotoCleaner
Delete Engine
Version 1.3.3
"""

from pathlib import Path

from send2trash import send2trash


class DeleteEngine:
    """
    ファイルをWindowsのごみ箱へ移動する
    """

    def move_to_trash(self, filepath):
        """
        1ファイルをごみ箱へ移動する

        Parameters
        ----------
        filepath : str
            ごみ箱へ移動するファイル

        Returns
        -------
        bool
            成功した場合True
        """

        path = Path(filepath)

        if not path.exists():
            return False

        if not path.is_file():
            return False

        try:

            send2trash(str(path))

            return True

        except Exception as error:

            print(
                f"ごみ箱への移動に失敗しました: "
                f"{path}"
            )

            print(error)

            return False

    def move_files_to_trash(self, filepaths):
        """
        複数ファイルをごみ箱へ移動する

        Parameters
        ----------
        filepaths : list
            ファイルパスのリスト

        Returns
        -------
        tuple
            (成功件数, 失敗件数, 失敗ファイル)
        """

        success_count = 0
        failure_count = 0
        failed_files = []

        for filepath in filepaths:

            if self.move_to_trash(filepath):

                success_count += 1

            else:

                failure_count += 1
                failed_files.append(filepath)

        return (
            success_count,
            failure_count,
            failed_files
        )