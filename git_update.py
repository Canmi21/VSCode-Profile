import os
import subprocess

# 检测是否存在 Git
def git_installed():
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# 更新仓库
def update_repositories(repo_urls):
    for url in repo_urls:
        print(f"正在更新仓库: {url}")
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", url], check=True)
        else:
            try:
                subprocess.run(["git", "remote", "add", "origin", url], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["git", "remote", "set-url", "origin", url], check=True)

        # 添加更改
        subprocess.run(["git", "add", "."], check=True)
        
        # 检查是否有更改
        result = subprocess.run(["git", "diff-index", "--quiet", "HEAD"], check=False)
        if result.returncode != 0:  # 有更改
            # 处理未暂存的更改
            status_result = subprocess.run(["git", "status", "--porcelain"], check=True, stdout=subprocess.PIPE, text=True)
            if status_result.stdout:
                print("检测到未暂存的更改，自动添加所有更改。")
                subprocess.run(["git", "add", "."], check=True)  # 再次添加更改
                subprocess.run(["git", "commit", "-m", "Update from script"], check=True)
                subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
            else:
                print("没有更改，跳过提交。")
        else:
            print("没有更改，跳过提交。")

# 主函数
def main():
    repo_file = "repositories.txt"

    if git_installed():
        if os.path.exists(repo_file):
            with open(repo_file, "r") as f:
                repo_urls = [line.strip() for line in f if line.strip()]
            update_repositories(repo_urls)
        else:
            new_repo_url = input("没有找到 repositories.txt 文件，请输入新的仓库地址: ")
            with open(repo_file, "w") as f:
                f.write(new_repo_url + "\n")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", new_repo_url], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
    else:
        print("未检测到 Git，请确保 Git 已安装。")

if __name__ == "__main__":
    main()
