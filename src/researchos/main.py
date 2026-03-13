"""Entrypoint for running the ROS skeleton pipeline."""

from __future__ import annotations

from researchos.ros_loop import ROSLoop


def main() -> None:
    question = "tea aroma volatile compounds review"
    ROSLoop(question).run()


if __name__ == "__main__":
    main()
