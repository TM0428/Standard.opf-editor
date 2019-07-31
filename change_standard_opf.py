kaigyo = "\n"

def change_standard_opf(path,title,title_yomi,author1,author1_yomi,author2,author2_yomi,publisher,publisher_yomi,description):
    f = open(path,'r',encoding="utf-8_sig")
    lines = f.readlines()
    lines_kai = []
    i_title_yomi = False
    i_author1 = False
    i_author2 = False
    i_publisher = False
    l_title_yomi = [line for line in lines if '<meta refines="#title" property="file-as">' in line]
    l_author1 = [line for line in lines if '<dc:creator id="creator01">' in line]
    l_author2 = [line for line in lines if '<dc:creator id="creator02">' in line]
    l_publisher = [line for line in lines if '<dc:publisher id="publisher">' in line]
    if l_title_yomi == [] and title_yomi != "":
        i_title_yomi = True
    if l_author1 == []:
        i_author1 = True
    if l_author2 == [] and author2 != "":
        i_author2 = True
    if l_publisher == [] and publisher != "":
        i_publisher = True    
    
    for line in lines:
        if line.startswith('<dc:title id="title">'):
            text = '<dc:title id="title">' + title + '</dc:title>\n'
            lines_kai.append(text)
            if i_title_yomi:
                text1 = '<meta refines="#title" property="file-as">' + title_yomi + '</meta>\n'
                lines_kai.append(text1)
                lines_kai.append(kaigyo)
            if i_author1:
                text1 = '<dc:creator id="creator01">' + author1 + '</dc:creator>\n'
                text2 = '<meta refines="#creator01" property="role" scheme="marc:relators">aut</meta>\n'
                text3 = '<meta refines="#creator01" property="file-as">' + author1_yomi + '</meta>\n'
                text4 = '<meta refines="#creator01" property="display-seq">1</meta>\n'
                lines_kai.append(text1)
                lines_kai.append(text2)
                lines_kai.append(text3)
                lines_kai.append(text4)
                lines_kai.append(kaigyo)
            if i_author2:
                text1 = '<dc:creator id="creator02">' + author2 + '</dc:creator>\n'
                text2 = '<meta refines="#creator02" property="role" scheme="marc:relators">aut</meta>\n'
                text3 = '<meta refines="#creator02" property="file-as">' + author2_yomi + '</meta>\n'
                text4 = '<meta refines="#creator02" property="display-seq">2</meta>\n'
                lines_kai.append(text1)
                lines_kai.append(text2)
                lines_kai.append(text3)
                lines_kai.append(text4)
                lines_kai.append(kaigyo)
            if i_publisher:
                text1 = '<dc:publisher id="publisher">' + publisher + '</dc:publisher>\n'
                lines_kai.append(text1)
                lines_kai.append(kaigyo)

        elif line.startswith('<meta refines="#title" property="file-as">') and not i_title_yomi:
            text = '<meta refines="#title" property="file-as">' + title_yomi + '</meta>\n'
            lines_kai.append(text)
        elif line.startswith('dc:creator') and not i_author1 and not i_author2:
            text = '<dc:creator id="creator01">' + author1 + '</dc:creator>\n'
            lines_kai.append(text)
        elif line.startswith('<meta refines="#creator01" property="file-as">') and not i_author1 and not i_author2:
            text = '<meta refines="#creator01" property="file-as">' + author1_yomi + '</meta>\n'
            lines_kai.append(text)
        elif line.startswith('<dc:publisher id="publisher">')and not i_publisher:
            text = '<dc:publisher id="publisher">' + publisher + '</dc:publisher>\n'
            lines_kai.append(text)
        elif line.startswith('<dc:language>'):
            lines_kai.append(line)
            lines_kai.append(kaigyo)
            text = '<dc:description>' + description + '</dc:description>\n'
            lines_kai.append(text)
        elif line.startswith('<dc:description>'):
            text = ''
        else:
            lines_kai.append(line)
    w = open(path, 'w',encoding = "utf-8_sig")
    w.writelines(lines_kai)
