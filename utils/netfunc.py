import json
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import shlex

class SendNetFunctions:
    def parseHeaders(self, header_text):
        headers = {}
        lines = header_text.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return headers

    def parseCookies(self, cookie_text):
        cookies = {}
        lines = cookie_text.split(';')
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies

    def parsePostData(self, post_text):
        posts = {}
        lines = post_text.split('&')
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                posts[key.strip()] = value.strip()
        return posts

    def parseUrlParams(self, url):
        parsed_url = urlparse(url)
        query_params = parsed_url.query
        if query_params:
            params_dict = parse_qs(query_params)
            for key in params_dict:
                params_dict[key] = params_dict[key][0]
            return True, params_dict
        else:
            return False, None

    def displayResponse(self, response_text, headers, cookies, time, statuscode, size):
        try:
            json_data = json.loads(response_text)
            formatted_text = json.dumps(json_data, indent=4, ensure_ascii=False)
        except json.JSONDecodeError:
            try:
                soup = BeautifulSoup(response_text, 'html.parser')
                formatted_text = soup.prettify()
            except:
                formatted_text = response_text

        current_time = datetime.now()
        current_hour = f"{current_time.hour:02d}"
        current_minute = f"{current_time.minute:02d}"
        current_second = f"{current_time.second:02d}"
        status_text = f"请求状态： {statuscode}    请求耗时：{time:.2f}秒    请求时间：{current_hour}:{current_minute}:{current_second}    响应大小：{size:.2f} KB"

        response_data = {
            'formatted_text': formatted_text,
            'status_text': status_text,
            'headers': headers,
            'cookies': cookies
        }
        return response_data

    def importCurl(self, curl_command):
        args = shlex.split(curl_command)
        url = None
        method = "GET"
        headers = {}
        cookies = {}
        data = None
        proxy = None

        i = 0
        while i < len(args):
            if args[i] == 'curl':
                i += 1
                continue
            if args[i].startswith('http'):
                url = args[i]
            elif args[i] == '-X':
                method = args[i+1]
                i += 1
            elif args[i] == '-H':
                header = args[i+1]
                key, value = header.split(':', 1)
                if key.strip().lower() == 'cookie':
                    cookie_parts = value.strip().split(';')
                    for part in cookie_parts:
                        if '=' in part:
                            cookie_key, cookie_value = part.split('=', 1)
                            cookies[cookie_key.strip()] = cookie_value.strip()
                else:
                    headers[key.strip()] = value.strip()
                i += 1
            elif args[i] == '--data' or args[i] == '--data-raw' or args[i] == '-d':
                data = args[i+1]
                method = "POST"
                i += 1
            elif args[i] == '--cookie':
                cookie = args[i+1]
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
                i += 1
            elif args[i] == '--proxy':
                proxy = args[i+1]
                i += 1
            i += 1

        return {
            'url': url,
            'method': method,
            'data': data,
            'headers': headers,
            'cookies': cookies,
            'proxy': proxy
        }

    def generate_code_for_language(self, language, url, method, headers, cookies, data, check_verify, check_allow_redirects):
        def is_json(data):
            try:
                json.loads(data)
                return True
            except ValueError:
                return False

        if language == "Python - Requests":
            code_lines = [
                "import requests",
                "",
                f'url = "{url}"',
                f'headers = {headers}',
            ]

            url_check, params = self.parseUrlParams(url)
            if url_check:
                url = url_check
                params = json.dumps(params, indent=4)
                code_lines.append(f'params = {params}')
            if cookies != '{}':
                code_lines.append(f'cookies = {cookies}')

            data_type = 'json' if is_json(data) else 'data'

            if data and data_type == "data":
                data = json.dumps(self.parsePostData(data), indent=4)
                code_lines.append(f'payload = {data}')
            elif data and data_type == "json":
                code_lines.append(f'payload = {data}')

            request_line = f'response = requests.request("{method}", url, headers=headers'
            if url_check:
                request_line += ', params=params'
            if cookies != '{}':
                request_line += ', cookies=cookies'
            if data:
                request_line += f', {data_type}=payload'
            if check_verify:
                request_line += f', verify=False'
            if check_allow_redirects:
                request_line += f', allow_redirects=False'
            request_line += ')'
            code_lines.append(request_line)

            code_lines.append('print(response.text)')

            code = "\n".join(code_lines)
        elif language == "PHP - cURL":
            code_lines = [
                "<?php",
                "$ch = curl_init();",
                f"curl_setopt($ch, CURLOPT_URL, '{url}');",
                'curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);',
                'curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);',
                "curl_setopt($ch, CURLOPT_ENCODING, '');",
                'curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);',
            ]
            if check_allow_redirects:
                code_lines.append('curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);')
            php_curl_array = []
            php_curl_array.append("$headers = [")
            headers_dict = json.loads(headers)
            for key, value in headers_dict.items():
                php_curl_array.append(f"    '{key}: {value}',")
            if cookies != "":
                php_curl_array.append(f"    'Cookie: {cookies}'")
            php_curl_array.append("];")
            php_curl_array.append("curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);")
            data_type = 'json' if is_json(data) else 'data'
            if data and data_type == "data":
                code_lines.append("curl_setopt($ch, CURLOPT_POST, 1);")
                code_lines.append(f"curl_setopt($ch, CURLOPT_POSTFIELDS, '{data}');")
            elif data and data_type == "json":
                code_lines.append("curl_setopt($ch, CURLOPT_POST, 1);")
                data_json = ["json_encode(["]
                items = list(json.loads(data).items())
                for i, (key, value) in enumerate(items):
                    if i == len(items) - 1:
                        data_json.append(f"'{key}' => '{value}'")
                    else:
                        data_json.append(f"'{key}' => '{value}', ")
                data_json.append("])")
                data = "".join(data_json)
                code_lines.append(f"curl_setopt($ch, CURLOPT_POSTFIELDS, {data});")
            code_lines.append("\n".join(php_curl_array))
            code_lines.append("$response = curl_exec($ch);")
            code_lines.append("if (curl_errno($ch)) {")
            code_lines.append(f"    print_r('cURL error: ' . curl_error($ch));")
            code_lines.append(f"    exit();")
            code_lines.append("}")
            code_lines.append("curl_close($ch);")
            code_lines.append("print_r($response);")
            code = "\n".join(code_lines)
        elif language == "Java - OKHttp":
            code_lines = [
                "import okhttp3.*;",
                "import java.io.IOException;",
                "import okhttp3.RequestBody;",
                "",
                "public class OkHttpExample {",
                "\tpublic static void main(String[] args) throws IOException {",
                f"\t\tString url = \"{url}\";",
                "\t\tOkHttpClient client = new OkHttpClient();",
                "\t\tRequest.Builder builder = new Request.Builder();",
                "\t\tbuilder.url(url);",
                "",
                "\t\tHeaders.Builder headersBuilder = new Headers.Builder();"
            ]

            headers_dict = json.loads(headers)
            for key, value in headers_dict.items():
                if "\"" in value:
                    value = value.replace("\"", "\\\"")
                code_lines.append(f"\t\theadersBuilder.add(\"{key}\", \"{value}\");")

            if cookies != "":
                code_lines.append(f"\t\theadersBuilder.add(\"Cookie\", \"{cookies}\");")

            code_lines.append("\t\tbuilder.headers(headersBuilder.build());")

            if data:
                data_type = 'json' if is_json(data) else 'data'
                if data_type == 'json':
                    code_lines.append(f"\t\tRequestBody body = RequestBody.create(MediaType.get(\"application/json; charset=utf-8\"), '{json.dumps(json.loads(data))}');")
                else:
                    code_lines.append(f"\t\tRequestBody body = RequestBody.create(MediaType.get(\"application/x-www-form-urlencoded\"), \"{data}\");")
                code_lines.append("\t\tbuilder.method(method.toUpperCase(), body);")
            else:
                code_lines.append("\t\tbuilder.method(method.toUpperCase(), null);")
            code_lines.extend([
                "\t\tRequest request = builder.build();",
                "\t\ttry (Response response = client.newCall(request).execute()) {",
                "\t\t\tSystem.out.println(response.code());",
                "\t\t\tSystem.out.println(response.body().string());",
                "\t\t}",
                "\t}",
                "}"
            ])

            code = "\n".join(code_lines)

        elif language == "Shell - cURL":
            code_lines = [
                "#!/bin/bash",
                f"url='{url}'",
                f"method='{method}'",
                "headers=()"
            ]

            headers_dict = json.loads(headers)
            for key, value in headers_dict.items():
                code_lines.append(f'headers+=("-H \"{key}: {value}\"")')

            if cookies != "":
                code_lines.append(f'headers+=("-H \"Cookie: {cookies}\"")')

            data_command = ""
            if data:
                data_type = 'json' if is_json(data) else 'data'
                if data_type == 'json':
                    code_lines.append(f"data='{json.dumps(json.loads(data))}'")
                    data_command = "--data \"$data\""
                else:
                    data_command = f"--data '{data}'"

            code_lines.extend([
                "curl_command=(curl --location --request $method \"$url\" \\\n\t\t${headers[@]}",
                f"\t\t{data_command})",
                "response=$(\"${curl_command[@]}\")",
                "exit_code=$?",
                "if [ $exit_code -ne 0 ]; then",
                "\techo \"cURL command failed with exit code $exit_code\"",
                "\texit $exit_code",
                "else",
                "\techo \"Response from server:\"",
                "\techo \"$response\"",
                "fi"
            ])

            code = "\n".join(code_lines)
        else:
            code = "Unsupported language"

        return code