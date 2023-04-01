import os
import getopt
import sys
import datetime
import json
import re
import shutil

def copy_dir(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)

        if os.path.isdir(src_path):
            copy_dir(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)


def log(log_str, log_lvl='I'):
    format_str = "[{}] {}: {}".format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), log_lvl, log_str)
    print(format_str)

class article():
    def __init__(self, jk_root, raw_article=''):
        self.title = ''
        self.jk_root = jk_root
        self.categories_str = ''
        self.categories = []
        self.author = ''

        self.private_dir = ['img', 'code', 'refs']

        self.title_file_used=''

        self.create_time = ''
        self.create_time_str = ''
        self.status = ''

        self.status = ''

        self.article_root_path = ''
        self.abs_article_root_path = ''

        self.article_path = ''
        self.abs_article_path = ''

        self.post_root_path = ''
        self.abs_post_root_path = ''
        self.post_path = ''
        self.abs_post_path = ''
        
        self.draft_root_path = ''
        self.abs_draft_root_path = ''
        self.draft_path = ''
        self.abs_draft_path = ''

        self.categories_path = []
        self.abs_categories_path = []
        self.categories_html_path = []
        self.abs_categories_html_path = []
        self.categories_html_post_path = []
        self.abs_categories_html_post_path = []

        if raw_article != '':
            self.abs_article_path = os.path.abspath(raw_article)
            self.read_header()
            self.get_all_paths_str()
            if self.abs_article_path != os.path.abspath(raw_article):
                if os.path.exists(self.abs_article_path):
                    log('{} already exists.'.format(self.abs_article_path), 'E')
                else:
                    log("Can't find nr_blog article, create one based on the the raw_article {}".format(os.path.abspath(raw_article)))
                    # new an empty article
                    self.new(title = self.title, author= self.author, categories = self.categories_str, status = 'none')
                    # copy article
                    shutil.copy(os.path.abspath(raw_article), self.abs_article_path)
            self.get_status()
            return
    
    def check_file(self):
        check_path = []
        # if os.path.exists(self.abs_article_root_path):
        #     log('check {} pass')
        return

    def get_status(self):
        if os.path.exists(self.abs_post_path):
            self.status = 'post'
        elif os.path.exists(self.abs_draft_path):
            self.status = 'draft'
        else:
            self.status = 'none'
        
        return self.status

    def get_all_paths_str(self):

        self.title = self.title.replace('\"', '').replace('\'', '')
        self.title_file_used = self.title.replace(' ', '-')

        if ' ' in self.categories_str:
            self.categories = self.categories_str.split(" ")
        else:
            self.categories = [self.categories_str]

        self.article_root_path = "sources/articles/{}/{}/".format(
            self.categories[0], self.title_file_used).replace(' ', '-')
        self.article_root_path = os.path.join(self.jk_root, self.article_root_path)
        self.abs_article_root_path = os.path.abspath(self.article_root_path)

        self.article_path = "sources/articles/{}/{}/{}.md".format(
            self.categories[0], self.title_file_used, self.title_file_used).replace(' ', '-')
        self.article_path = os.path.join(self.jk_root, self.article_path)
        self.abs_article_path = os.path.abspath(self.article_path)

        self.post_root_path = os.path.join(self.jk_root, '_posts')
        self.abs_post_root_path = os.path.abspath(self.post_root_path)

        self.post_path = '_posts/{}-{}.md'.format(
            self.create_time.strftime("%Y-%m-%d"), self.title_file_used)
        self.post_path = os.path.join(self.jk_root, self.post_path)
        self.abs_post_path = os.path.abspath(self.post_path)

        self.draft_root_path = os.path.join(self.jk_root, '_drafts')
        self.abs_draft_root_path = os.path.abspath(self.draft_root_path)
        self.draft_path = '_drafts/{}-{}.md'.format(
            self.create_time.strftime("%Y-%m-%d"), self.title_file_used)
        self.abs_draft_path = os.path.join(self.jk_root, self.draft_path)

        self.categories_path = []
        self.abs_categories_path = []
        self.categories_html_path = []
        self.abs_categories_html_path = []
        self.categories_html_post_path = []
        self.abs_categories_html_post_path = []

        for (i, it) in enumerate(self.categories):
            tmp_path = 'sources/articles/{}/'.format(it)
            tmp_path = os.path.join(self.jk_root, tmp_path)
            self.categories_path.append(tmp_path)
            self.abs_categories_path.append(os.path.abspath(tmp_path))

            tmp_path = 'sources/articles/{}/{}.html'.format(it, it)
            tmp_path = os.path.join(self.jk_root, tmp_path)
            self.categories_html_path.append(tmp_path)
            self.abs_categories_html_path.append(os.path.abspath(tmp_path))

            tmp_path = '_posts/1996-1-1-{}.html'.format(it)
            tmp_path = os.path.join(self.jk_root, tmp_path)
            self.categories_html_post_path.append(tmp_path)
            self.abs_categories_html_post_path.append(
                os.path.abspath(tmp_path))

    def gen_header(self):
        format_str = \
'''---
layout: default
title: {}
categories: {}
author: {}
create_time: {}
---'''.format(
            self.title,
            self.categories_str,
            self.author,
            self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        )

        return format_str

    def write_header(self):
        return

    def read_header(self):
        val_map = {'author': 'author',
                   'categories': 'categories_str',
                   'create_time': 'create_time_str',
                   'title': 'title'}

        with open(self.abs_article_path, 'r') as fd:
            ln = fd.readline()
            ln = ln.replace('\r', '').replace('\n', '')
            if ln != '---' :
                info_str = '{} is not a nr_blog article'.format(self.abs_article_path)
                log(info_str)
                raise Exception(info_str)
                return

            while True:
                ln = fd.readline()
                ln = ln.replace('\r', '').replace('\n', '')

                if ln == '---\n' or ln == '':
                    break
                re_ans = re.findall("^(\S+)\:\s+(.*)", ln)
                if len(re_ans):
                    key_name = re_ans[0][0]
                    val = re_ans[0][1]
                    if key_name in val_map.keys():
                        setattr(self, val_map[key_name], val)

            for key in val_map.keys():
                it = val_map[key]
                if getattr(self, it) == '':
                    info_str = 'Can not read header for missing {} in the file {}.'.format(key, self.abs_article_path)
                    log(info_str)
                    raise Exception(info_str)
            
            self.create_time = datetime.datetime.strptime(self.create_time_str, "%Y-%m-%d %H:%M:%S")
        return

    def read_context(self, path = ''):
        if path == '':
            path = self.abs_article_path

        with open(path, 'r') as fd:
            lines = fd.readlines()
            if lines[0].replace('\r', '').replace('\n', '') != '---':
                return lines
            else:
                for i in range(1, len(lines)):
                    if lines[i].replace('\r', '').replace('\n', '') == '---':
                        break
                return lines[i+1:]

    def new(self, title, author = 'nrush', categories='none', status="none", raw_article = '', img = '', code = '', refs = ''):
        self.title = title
        self.status = status
        self.author = author
        self.create_time = datetime.datetime.now()
        self.categories_str = categories

        self.get_all_paths_str()

        # create category-html files
        for (i, it) in  enumerate(self.categories):
            if os.path.exists(self.abs_categories_html_path[i]) == False:
                os.makedirs(self.abs_categories_path[i])
                with open(os.path.join(self.jk_root, 'sources/articles/category_template'), 'r') as fd_in:
                    with open(self.abs_categories_html_path[i], 'w') as fd_out:
                        for (num, ln) in enumerate(fd_in):
                            ln = ln.replace("<title>", self.categories[0])
                            fd_out.write(ln)

        # create article
        if os.path.exists(self.abs_article_path) == False:
            os.makedirs(self.abs_article_root_path)
            with open(self.abs_article_path, 'w') as fd_out:
                header = self.gen_header()
                fd_out.write(header)
                fd_out.write("\n<center><strong><font size=6>Create a blog website based on jekyll</font></strong></center>\n")
                fd_out.write("\n- this unordered seed list will be replaced by toc as unordered list\n")
                fd_out.write("{:toc}\n")
                fd_out.write("\n## Reference\n")

            for it in self.private_dir:
                src_path = locals()[it]
                if src_path != '':
                    copy_dir(src_path, os.path.join(self.abs_article_root_path, it))
                else:
                    os.makedirs(os.path.join(self.abs_article_root_path, it))
                
            if os.path.exists(raw_article):
                ctx = self.read_context(raw_article)
                with open(self.abs_article_path, 'w') as fd_out:
                    header = self.gen_header()
                    fd_out.write(header)
                    tmp_str = ''
                    for ln in ctx:
                        tmp_str = tmp_str + ln
                    fd_out.write(tmp_str)
        return

    def delete(self):
        if os.path.exists(self.abs_article_root_path):
            if self.status == 'post':
                self.unpost()
            elif self.status == 'draft':
                self.undraft()
            shutil.rmtree(self.abs_article_root_path)
        return

    def post(self):
        self.get_status()
        if self.status == 'draft':
            os.remove(self.abs_draft_path)
        
        if os.path.exists(self.abs_post_path):
            return
        
        if self.status == 'none':
            symlink_path = os.path.relpath(self.abs_article_path, self.abs_post_root_path)
            os.symlink(symlink_path, self.abs_post_path)
            for i in range(len(self.categories)):
                cate_post_path = self.abs_categories_html_post_path[i]
                html_path = self.abs_categories_html_path[i]
                if os.path.exists(cate_post_path) == False:
                    symlink_path = os.path.relpath(html_path, self.abs_post_root_path)
                    os.symlink(symlink_path, cate_post_path)
            self.status = 'post'
        return

    def unpost(self):
        if os.path.exists(self.abs_post_path):
            os.remove(self.abs_post_path)
            self.get_status()
            return
    
    def draft(self):
        self.get_status()
        if self.status == 'post':
            os.remove(self.abs_post_path)
        
        if os.path.exists(self.abs_draft_path):
            return
        
        if self.status == 'none':
            symlink_path = os.path.relpath(self.abs_article_path, self.abs_draft_root_path)
            os.symlink(symlink_path, self.abs_draft_path)
            self.status = 'draft'
        return

    def undraft(self):
        if os.path.exists(self.abs_draft_path):
            os.remove(self.abs_post_root_path)
            self.get_status()
            return

    def __str__(self) -> str:
        format_str = ""
        return format_str

class category():
    def __init_():
        return

class site():
    def __init__(self, root_path) -> None:
        self.root_path = root_path
        self.abs_root_path = os.path.abspath(self.root_path)

        self.articles_path = os.path.join(self.root_path, 'sources/articles')
        self.abs_articles_path = os.path.abspath(self.articles_path)
        self.articles = {}
        self.categories = {}

        category_dirs = os.listdir(self.abs_articles_path)
        for it in category_dirs:
            category_dir = os.path.join(self.articles_path, it)
            if os.path.isdir(category_dir) == True:
                articles_dirs = os.listdir(category_dir)
                for it1 in articles_dirs:
                    article_dir = os.path.join(category_dir, it1)
                    if os.path.isdir(article_dir) == False:
                        continue
                    article_path = os.path.join(article_dir, "{}.md".format(it1))
                    try:
                        art = article(self.root_path, article_path)
                    except:
                        log("Failed to get the info of {}".format(article_path))
                        continue

                    self.articles[art.title] = art
                    for cate in art.categories:
                        if cate not in self.categories:
                            self.categories[cate] = [art]
                        else:
                            self.categories[cate].append(art)
        pass

    def new(self, title, categories, author):
        art = article(jk_root=self.root_path)
        art.new(title, author, categories)
        return

    def delete(self, title, force=False):
        if title in self.articles.keys():
            art = self.articles[title]
            if force == False:
                ans = input("Do you really want to delete \'{}\'? (Y/N)".format(title))
                if ans != 'Y':
                    return
            art.delete()
        else:
            log("\'{}\' is unknown.".format(title), 'E')
        return

    def post(self, title):
        if title in self.articles.keys():
            art = self.articles[title]
            art.post()
        else:
            log("\'{}\' is unknown.".format(title), 'E')
        return

    def unpost(self, title):
        if title in self.articles.keys():
            art = self.articles[title]
            art.unpost()
        else:
            log("\'{}\' is unknown.".format(title), 'E')
        return
    
    def draft(self, title):
        if title in self.articles.keys():
            art = self.articles[title]
            art.draft()
        else:
            log("\'{}\' is unknown.".format(title), 'E')
        return
    
    def undraft(self, title):
        if title in self.articles.keys():
            art = self.articles[title]
            art.undraft()
        else:
            log("\'{}\' is unknown.".format(title), 'E')
        return

    def list(self):
        print("{:<48} {:<16} {:<6} {:<20} {}".format("title", "author", "status", "create_time", "categories"))
        print(100*"-")
        for key in self.articles.keys():
            art = self.articles[key]
            print("{:<48} {:<16} {:<6} {:<20} {}".format("\'" + art.title + "\'", art.author, art.status, art.create_time_str, art.categories_str))
        return

    def import_article(self, title, author, categories, article_path, img, code, refs):
        if title in self.articles.keys():
            log("\'{}\' already exists.".format(title), 'E')
        else:
            art = article(self.root_path)
            art.new(title=title,
                    author=author,
                    categories=categories,
                    raw_article=article_path,
                    img=img,
                    code=code,
                    refs=refs
                    )
        return

def usage():
    # blg import -t <article new name> -t <title> -c '<categories>' -a <author> --article=<article_path> --img=<img_soures> --code=<code_soures> --refs=<refs_source>
    # blg new -t <title> -c '<categories>' -a <author>
    # blg del -t <title>
    # blg post -t <title>
    # blg unpost -t <title>
    # blg list
    # blg init
    return "python blg re"

if __name__ == '__main__':
    force = False
    src_article = ''
    img = ''
    code = ''
    refs = ''
    author = 'Nrush'
    categories = 'none'
    opts,args = getopt.getopt(sys.argv[2:], "t:c:a:f", ["src_article=", "img=", "code=", "refs="])
    for name, val in opts:
        if name == '-t':
            title = val
        elif name == '-c':
            categories = val
        elif name == '-a':
            author = val
        elif name == '-f':
            force = True
        elif name == '--src_article':
            src_article = val
        elif name == '--img':
            img = val
        elif name == '--code':
            code = code
        elif name == '--refs':
            refs = val

    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, 'config.json'), 'r') as fd:
        config = json.load(fd)

    sit = site(config['jk_root'])
    if sys.argv[1] == 'new':
        sit.new(title, categories, author)
    elif sys.argv[1] == 'del':
        sit.delete(title, force)
    elif sys.argv[1] == 'post':
        sit.post(title)
    elif sys.argv[1] == 'unpost':
        sit.unpost(title)
    elif sys.argv[1] == 'draft':
        sit.draft(title)
    elif sys.argv[1] == 'undraft':
        sit.undraft(title)
    elif sys.argv[1] == 'list':
        sit.list()
    elif sys.argv[1] == 'import':
        sit.import_article(title, author, categories, src_article, img, code, refs)