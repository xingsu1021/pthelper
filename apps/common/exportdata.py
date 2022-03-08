import xlwt
import io
import json
from django.http import HttpResponse

#导出Excel表格
def get_excel_stream(file):
    # StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。
    excel_stream = io.BytesIO()
    # 这点很重要，传给save函数的不是保存文件名，而是一个BytesIO流（在内存中读写）
    file.save(excel_stream)
    # getvalue方法用于获得写入后的byte将结果返回给re
    res = excel_stream.getvalue()
    excel_stream.close()
    return res
def export_excel(data, name,header):
    # 打开一个Excel工作簿
    file = xlwt.Workbook()
    # 新建一个sheet，如果对一个单元格重复操作，会引发异常，所以加上参数cell_overwrite_ok=True
    table = file.add_sheet(name, cell_overwrite_ok=True)
    if data is None:
        return file
    # 表示行
    l = 0 
    n = len(header)
    # 将data中的数据依次写入到table中
    for line in data:
        for i in range(n):
            table.write(l, i, line[header[i]])
        l += 1
    # 获取将数据保存到流
    res=get_excel_stream(file)
    # 返回一个response响应
    response = HttpResponse(content_type='application/vnd.ms-excel')
    from urllib import parse
    response['Content-Disposition'] = 'attachment;filename=' + parse.quote(excel_name) + '.xls'
    # 将文件流写入到response返回
    response.write(res)
    return response

#导出json文件
def get_stream(item):
    # 开始这里我用ByteIO流总是出错，但是后来参考廖雪峰网站用StringIO就没问题
    file = io.StringIO()
    data=json.dumps(data)
    file.write(data)
    res=file.getvalue()
    file.close()
    return res
def export_json(item):
    try:
        json_stream=get_stream(item)
        response = HttpResponse(content_type='application/json')
        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(file_name) + '.json'
        response.write(json_stream)
        return response
    except Exception as e:
        logging.error(e)
        print(e)

#导出压缩包        
def write_zip(e_data, j_data, export_name):
    try:
        # 保存到本地文件
        # 返回文件名，注意此时保存的方法和前面导出保存的json、excel文件区别
        j_name = write_json(j_data, export_name[1])
        e_name = write_excel(e_data, export_name[1])
        # 本地文件写入zip，重命名，然后删除本地临时文件
        z_name='export.zip'
        z_file = zipfile.ZipFile(z_name, 'w')
        z_file.write(j_name)
        z_file.write(e_name)
        os.remove(j_name)
        os.remove(e_name)
        z_file.close()
        # 再次读取zip文件，将文件流返回,但是此时打开方式要以二进制方式打开
        z_file = open(z_name, 'rb')
        data = z_file.read()
        z_file.close()
        os.remove(z_file.name)
        response = HttpResponse(data, content_type='application/zip')
        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(z_name)
        return response
    except Exception as e:
        logging.error(e)
        print(e)