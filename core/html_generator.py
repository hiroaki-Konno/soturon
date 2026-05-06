import os
import pathlib
import zipfile

_BASE_HTML = """\
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{ margin: 0; font-family: sans-serif; }}
    h1 {{ margin: 16px 0 16px 24px; font-size: 2rem; }}
    .score-img {{ width: 100%; vertical-align: top; display: block; }}
    .lyric {{ margin: 8px 24px; font-size: 1rem; color: #333; white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
{body}
</body>
</html>
"""


class HtmlGenerator:
    def __init__(self, title: str, image_paths: list, lyrics: dict = None):
        """
        Parameters
        ----------
        title : str
            楽譜タイトル
        image_paths : list[str]
            img src に使うパス（HTMLから見た相対パスを推奨）
        lyrics : dict[int, str], optional
            {画像インデックス: テキスト} — 対応画像の直後に <p> を挿入
        """
        self.title = title
        self.image_paths = image_paths
        self.lyrics = lyrics or {}

    def build(self) -> str:
        """HTML文字列を生成して返す"""
        lines = []
        for i, path in enumerate(self.image_paths):
            lines.append(f'  <img class="score-img" src="{path}" alt="{i + 1}">')
            if i in self.lyrics:
                text = (self.lyrics[i]
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"))
                lines.append(f'  <p class="lyric">{text}</p>')
        return _BASE_HTML.format(title=self.title, body="\n".join(lines))

    def save(self, output_path: str) -> str:
        """HTMLを output_path に保存し、絶対パスを返す"""
        parent = os.path.dirname(output_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.build())
        return os.path.abspath(output_path)

    def to_pdf(self, output_path: str, image_dir: str = None) -> str:
        """HTMLをPDFに変換して output_path に保存し、絶対パスを返す

        Parameters
        ----------
        output_path : str
            生成する PDF ファイルのパス
        image_dir : str, optional
            画像の相対パスを解決するフォルダ（省略時は output_path と同じフォルダ）
        """
        from weasyprint import CSS, HTML

        base_dir = image_dir or os.path.dirname(os.path.abspath(output_path))
        base_url = pathlib.Path(base_dir).as_uri() + "/"

        # ページ設定: A4縦、マージンなし、各画像を1ページに収める
        pdf_css = CSS(string="""
            @page { size: A4; margin: 0; }
            .score-img { width: 100%; height: auto; page-break-after: always; }
            .score-img:last-of-type { page-break-after: auto; }
            h1 { page-break-after: avoid; margin: 8px 0 4px 12px; font-size: 1.2rem; }
        """)

        parent = os.path.dirname(output_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        HTML(string=self.build(), base_url=base_url).write_pdf(
            output_path, stylesheets=[pdf_css]
        )
        return os.path.abspath(output_path)

    def to_zip(self, image_dir: str, output_path: str) -> str:
        """HTMLと image_dir 内の画像を ZIP 化して保存し、絶対パスを返す

        Parameters
        ----------
        image_dir : str
            ZIP に含める画像が格納されているフォルダ
        output_path : str
            生成する ZIP ファイルのパス
        """
        html_content = self.build()
        html_filename = f"{self.title}.html"

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(html_filename, html_content.encode("utf-8"))
            for img_path in self.image_paths:
                full = os.path.join(image_dir, img_path) if not os.path.isabs(img_path) else img_path
                if os.path.isfile(full):
                    zf.write(full, os.path.basename(img_path))

        return os.path.abspath(output_path)
