#!/usr/bin/env python3
"""Build the repository README from the Git history.

A problem is counted once when a commit touches a Python file directly under an
LV<number> directory.  Older history is backfilled conservatively using commit
subjects so that files that were unfinished when this dashboard was introduced
do not inflate the score.
"""

from __future__ import annotations

import os
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
SEOUL = ZoneInfo("Asia/Seoul")
GOAL = 5
# From the day this dashboard was introduced, committing an LV file is enough.
# Older commits need a solve-like subject so unfinished seed files stay excluded.
AUTO_TRACK_FROM = date(2026, 8, 11)
SOLVED_WORDS = re.compile(r"(?:solve|solved|solving|풀이|풀었|해결)", re.IGNORECASE)
PROBLEM_FILE = re.compile(r"^(LV\d+)/([^/]+)\.py$")
IGNORED_NAMES = {"test", "_템플릿", "template"}
AUTOMATION_SUBJECT = "docs: update coding challenge log"
WEEKDAYS = "월화수목금토일"


@dataclass(frozen=True)
class Commit:
    sha: str
    when: datetime
    author: str
    email: str
    subject: str
    files: tuple[str, ...]


@dataclass(frozen=True)
class SolvedProblem:
    path: str
    level: str
    name: str
    commit: Commit


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def read_commits() -> list[Commit]:
    # Record and field separators are control characters unlikely to occur in
    # ordinary commit subjects or paths.
    raw = git(
        "-c",
        "core.quotepath=false",
        "log",
        "--reverse",
        "--date=iso-strict",
        "--pretty=format:%x1e%H%x1f%aI%x1f%an%x1f%ae%x1f%s",
        "--name-only",
    )
    commits: list[Commit] = []
    for record in raw.split("\x1e"):
        record = record.strip()
        if not record:
            continue
        lines = record.splitlines()
        fields = lines[0].split("\x1f")
        if len(fields) != 5:
            continue
        sha, timestamp, author, email, subject = fields
        if (
            author == "github-actions[bot]"
            or email.endswith("@users.noreply.github.com") and "[bot]" in email
            or subject.startswith(AUTOMATION_SUBJECT)
        ):
            continue
        files = tuple(line.strip() for line in lines[1:] if line.strip())
        commits.append(
            Commit(
                sha=sha,
                when=datetime.fromisoformat(timestamp).astimezone(SEOUL),
                author=author,
                email=email,
                subject=subject,
                files=files,
            )
        )
    return commits


def solved_problems(commits: list[Commit]) -> list[SolvedProblem]:
    solved: list[SolvedProblem] = []
    seen: set[str] = set()
    for commit in commits:
        is_automatic_period = commit.when.date() >= AUTO_TRACK_FROM
        if not is_automatic_period and not SOLVED_WORDS.search(commit.subject):
            continue
        for path in commit.files:
            match = PROBLEM_FILE.match(path)
            if not match or path in seen:
                continue
            level, stem = match.groups()
            if stem.lower() in IGNORED_NAMES:
                continue
            seen.add(path)
            solved.append(
                SolvedProblem(
                    path=path,
                    level=level,
                    name=stem.replace("_", " "),
                    commit=commit,
                )
            )
    return solved


def repository_url() -> str:
    github_repository = os.getenv("GITHUB_REPOSITORY")
    if github_repository:
        return f"https://github.com/{github_repository}"
    try:
        remote = git("remote", "get-url", "origin")
    except subprocess.CalledProcessError:
        return ""
    if remote.startswith("git@github.com:"):
        remote = "https://github.com/" + remote.removeprefix("git@github.com:")
    return remote.removesuffix(".git")


def week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


def face(count: int) -> str:
    if count >= 6:
        return "🤩 목표 초과"
    if count == GOAL:
        return "😄 목표 달성"
    if count >= 3:
        return "🙂 목표가 보여요"
    if count >= 1:
        return "😢 조금 더 힘내기"
    return "😭 아직 시작 전"


def progress(count: int) -> str:
    return "🟩" * min(count, GOAL) + "⬜" * max(GOAL - count, 0)


def commit_link(repo: str, commit: Commit, head_sha: str) -> str:
    # The post-commit hook amends HEAD after generating the README.  Embedding
    # HEAD's SHA would change that SHA and leave a broken self-reference.
    if commit.sha == head_sha:
        return "`현재 커밋`"
    label = commit.sha[:7]
    return f"[{label}]({repo}/commit/{commit.sha})" if repo else f"`{label}`"


def problem_link(problem: SolvedProblem) -> str:
    return f"[{problem.name}]({quote(problem.path)})"


def generate() -> str:
    commits = read_commits()
    solved = solved_problems(commits)
    today = datetime.now(SEOUL).date()
    repo = repository_url()
    head_sha = git("rev-parse", "HEAD")

    solved_by_week: dict[date, list[SolvedProblem]] = defaultdict(list)
    solved_by_day: dict[date, list[SolvedProblem]] = defaultdict(list)
    commits_by_day: dict[date, list[Commit]] = defaultdict(list)
    for commit in commits:
        commits_by_day[commit.when.date()].append(commit)
    for problem in solved:
        solved_by_week[week_start(problem.commit.when.date())].append(problem)
        solved_by_day[problem.commit.when.date()].append(problem)

    current_start = week_start(today)
    current_count = len(solved_by_week[current_start])
    levels = Counter(problem.level for problem in solved)
    level_summary = " · ".join(
        f"**{level}** {levels[level]}문제"
        for level in sorted(levels, key=lambda item: int(item[2:]))
    ) or "아직 완료 기록 없음"

    first_day = min((commit.when.date() for commit in commits), default=today)
    active_days = len(commits_by_day)
    lines = [
        "# 🐣 꾸준한 코딩테스트 챌린지",
        "",
        "> 프로그래머스 **주 5문제**를 무리하지 않고 꾸준히 풉니다. 작은 기록을 오래 이어가는 것이 목표입니다.",
        "",
        "## 이번 주",
        "",
        f"### {progress(current_count)} {current_count} / {GOAL}문제 · {face(current_count)}",
        "",
        f"`{current_start:%Y.%m.%d} ~ {(current_start + timedelta(days=6)):%Y.%m.%d}`",
        "",
        f"누적 **{len(solved)}문제** · {level_summary} · 커밋한 날 **{active_days}일**",
        "",
        "> 표정 규칙: 0문제 `😭` · 1~2문제 `😢` · 3~4문제 `🙂` · 5문제 `😄` · 6문제 이상 `🤩`",
        "",
        "## 주간 기록",
        "",
        "| 주차 | 진행도 | 푼 문제 | 표정 |",
        "|---|:---:|---:|:---:|",
    ]

    cursor = current_start
    first_week = week_start(first_day)
    while cursor >= first_week:
        count = len(solved_by_week[cursor])
        end = cursor + timedelta(days=6)
        marker = " **(이번 주)**" if cursor == current_start else ""
        lines.append(
            f"| {cursor:%Y.%m.%d} ~ {end:%m.%d}{marker} | {progress(count)} | **{count} / {GOAL}** | {face(count).split()[0]} |"
        )
        cursor -= timedelta(days=7)

    lines.extend(
        [
            "",
            "## 날짜별 풀이와 커밋",
            "",
            "| 날짜 | 푼 문제 | 레벨 | 커밋 |",
            "|---|---|:---:|---|",
        ]
    )
    cursor = today
    while cursor >= first_day:
        day_commits = commits_by_day.get(cursor, [])
        day_solved = solved_by_day.get(cursor, [])
        solved_text = "<br>".join(problem_link(problem) for problem in day_solved) or "—"
        levels_text = "<br>".join(problem.level for problem in day_solved) or "—"
        commits_text = "<br>".join(
            f"{commit_link(repo, commit, head_sha)} {commit.subject}"
            for commit in day_commits
        ) or "—"
        lines.append(
            f"| {cursor:%Y.%m.%d} ({WEEKDAYS[cursor.weekday()]}) | {solved_text} | {levels_text} | {commits_text} |"
        )
        cursor -= timedelta(days=1)

    lines.extend(
        [
            "",
            "## 기록 기준",
            "",
            f"- `{AUTO_TRACK_FROM:%Y.%m.%d}`부터 `LV숫자/문제이름.py`를 커밋하고 push하면 커밋 메시지와 관계없이 자동으로 기록합니다.",
            "- 같은 문제는 처음 완료한 한 번만 집계하며 `test.py`, `_템플릿.py`는 제외합니다.",
            "- README는 문제를 커밋할 때 자동 갱신되어 같은 커밋에 포함됩니다.",
            "",
            "<!-- 이 파일의 학습 기록은 scripts/update_readme.py가 자동 생성합니다. -->",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    (ROOT / "README.md").write_text(generate(), encoding="utf-8")
