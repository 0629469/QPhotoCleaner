"""
QPhotoCleaner
Delete Engine
Version 2.0.0
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

    def move_files_to_trash(
        self,
        filepaths,
        progress_callback=None
    ):
        """
        複数ファイルをごみ箱へ移動する

        Parameters
        ----------
        filepaths : list
            ファイルパスのリスト

        progress_callback : callable, optional
            処理状況を通知するコールバック

            callback(
                processed,
                total,
                filepath,
                success
            )

        Returns
        -------
        tuple
            (成功件数, 失敗件数, 失敗ファイル)
        """

        success_count = 0
        failure_count = 0
        failed_files = []

        total = len(filepaths)

        for processed, filepath in enumerate(
            filepaths,
            start=1
        ):

            success = self.move_to_trash(
                filepath
            )

            if success:

                success_count += 1

            else:

                failure_count += 1
                failed_files.append(filepath)

            # -------------------------------------------------
            # GUIへ進捗を通知
            # -------------------------------------------------

            if progress_callback is not None:

                try:

                    progress_callback(
                        processed,
                        total,
                        filepath,
                        success
                    )

                except Exception as error:

                    print(
                        "進捗通知に失敗しました:"
                    )

                    print(error)

        return (
            success_count,
            failure_count,
            failed_files
        )