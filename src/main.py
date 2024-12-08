import json
import subprocess

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)


def get_commits(repo_path, date_limit):
    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%H %P", f"--before={date_limit}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = result.stdout.strip().splitlines()
    return [line.split() for line in commits]  # Returns list of [commit_hash, date]

def build_dependency_graph(repo_path, commits):
    graph = "graph TD\n"
    for commit_info in commits:
        commit_hash = commit_info[0]
        parents = commit_info[1:]
        for parent in parents:
            graph += f"    {commit_hash} --> {parent}\n"
    return graph


def save_graph(output_path, graph):
    with open(output_path, 'w') as f:
        f.write(graph)


def main():
    config = load_config('E:/Code/Projects/JetBrainsProjects/PycharmProjects/git_commit_visualiser/resources/config.json')
    repo_path = config["repo_path"]
    output_path = config["output_path"]
    date_limit = config["date_limit"]

    # Step 2: Get commits and build graph
    commits = get_commits(repo_path, date_limit)
    graph = build_dependency_graph(repo_path, commits)

    # Step 4: Save and output graph
    save_graph(output_path, graph)
    print(graph)


if __name__ == "__main__":
    main()
