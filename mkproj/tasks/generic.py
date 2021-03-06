from .. import templates
from ..bases import BaseTask
from ..core import depends
from ..subprocess import call


class MakeProjectDir(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "make-project-dir"

    @staticmethod
    def lang_id() -> str:
        return "generic"

    def _run(self) -> str:
        self._data["project-path"].mkdir()
        return "Created project directory at: {}".format(
            self._data["project-path"].absolute()
        )


@depends("make-project-dir")
class MakeReadme(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "make-readme"

    @staticmethod
    def lang_id() -> str:
        return "generic"

    def _run(self) -> str:
        with open(
            "{0}/README.md".format(str(self._data["project-path"].absolute())), "w"
        ) as file:
            templates.write_to_file(
                file, templates.get_template("generic", "README.md"), self._data
            )
        return "README created in {}".format(self._data["project-path"].absolute())


@depends("make-project-dir")
class GitInit(BaseTask):
    @staticmethod
    def task_id() -> str:
        return "git-init"

    @staticmethod
    def lang_id() -> str:
        return "generic"

    def _run(self) -> str:
        call(["git", "-C", self._data["project-path"].absolute(), "init"])
        return "Project initialized with git"
