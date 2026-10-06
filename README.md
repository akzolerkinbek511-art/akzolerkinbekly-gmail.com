# 46-тапсырма: CI-де тест (GitHub Actions)

Файл: `.github/workflows/ci.yml`

## Не істейді
1. Push / PR кезінде:
   - Ruff + Black (линт)
   - pytest + coverage
   - Docker image build
2. Coverage есебі Codecov-қа жіберіледі
3. README-де жасыл бэйдж үшін:
   ```
   ![CI](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)
   ```

## Жергілікті тексеру
```bash
pytest --cov=. --cov-report=term-missing -v
docker build -t foodexpress:local .
```
