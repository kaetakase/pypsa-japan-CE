# 日本9地域 PyPSAモデル（2040年度）GitHub公開候補

このZIPは、提供された `japan9cewg2(2).py`、`input 2.zip`、`results(1).zip` をもとに整理したものです。**論文の完全再計算による検証は未実施**です。

## 主なファイル

- `src/japan9cewg2.py`：提供されたPythonコードそのもの。最適化式は改変していません。
- `input/`：WGのコストを既定とする入力。既定の政策制約はOFF（誤作動防止）。
- `scenario_data/`：REIコスト（新版）。
- `cases.json`：WG、REI、WG-CO2、REI-CO2、WG-SEP、REI-SEPの制約条件。
- `scripts/run_case.py`：6ケースを間違えず準備・実行するためのラッパー。
- `reference_results/`：元の結果CSV（一切数値を変更していません）と図表再集計資料。
- `scripts/verify_reference.py`：論文の主要数値と元結果を照合する静的チェック。
- `scripts/compare_re_run.py`：再実行した結果と元結果を比較。

## 実行手順

```bash
python -m pip install -r requirements.txt
python scripts/verify_reference.py
# 6ケースからREI-CO2を選んで入力を準備する（計算はしない）
python scripts/run_case.py REI-CO2 --prepare-only
# 実際に8760時間の最適化を実行する
python scripts/run_case.py REI-CO2 --run --overwrite
# 計算が終わったら元結果と比較する
python scripts/compare_re_run.py REI-CO2
# 代表4週の計算（図2・図3用）
python scripts/run_case.py REI-CO2 --time-mode rep4 --run --overwrite
python scripts/compare_re_run.py REI-CO2 --time-mode rep4
```

`--prepare-only` はモデルを実行しません。成果物はGitに含めない `.work/` 以下に作成されます。元のPythonは既定で代表4週なので、直接起動せず上記のラッパー経由で実行してください。

## 確認済み／未確認

- 6ケースのシステムコスト、CO₂原単位、CO₂シャドウプライス、表7、表8の主要数値は元の結果CSVと整合。
- 代表週4・8・10週の年間システムコストは10.1、9.5、9.7兆円/年（論文図3の丸め値と整合）。
- 図4の発電電力量構成比（％）については、8760時間計算の元データとの整合性を確認済み。発電電力量の参照データは `reference_results/corrected_generation_TWh.csv` に収録している。過去の作図用データとの照合結果は `reference_results/figure4_correction_check.csv` に記録している。
- 元結果ファイルの一部の `SCENARIO_NAME` にWG/REIの表示違いがあるため、GitHub公開用の新しい実行ではラッパーが適切なケース名を付与します。
- 元結果とPython・入力からの完全な再計算一致は、PyPSA・HiGHS実行環境で6ケースと代表週を再実行して確認してください。
- **GitHubの現行ブランチとの比較・書き換えは実施していません。** 上書き前に既存リポジトリをバックアップし、新しいレビュー用ブランチで変更内容を確認してください。
- 公開前に、コードの利用許諾と元データの再配布権限を確認してください（`LICENSE_REVIEW_REQUIRED.md`）。

既存の `kaetakase/pypsa-japan-capacity-expansion` を置き換える場合は、`docs/GITHUB_REPLACEMENT_STEPS.md` に記したバックアップとレビュー用ブランチの手順を参照してください。既存リポジトリそのものには変更を加えていません。


## 2026-11-03: CO2制約OFFケースの設定修正

元モデルは、`policy_2040.csv` に `co2_intensity_tco2_per_mwh` というキーが存在すると、`use_co2_intensity_constraint=FALSE` であっても制約をONにします。このため、WGとREIでは当該キーを**書き込まない**よう `scripts/run_case.py` を修正し、`input/policy_2040.csv` からも削除しました。公開前に `python scripts/check_case_policy.py` で6ケースを確認してください。参照結果CSVは変更していません。
