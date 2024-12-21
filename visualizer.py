import argparse
import pkg_resources
from collections import defaultdict


def get_dependencies(package_name):
    """Получаем зависимости пакета и его транзитивные зависимости."""
    dependencies = defaultdict(set)

    try:
        # Получаем список установленных пакетов
        installed_packages = pkg_resources.working_set
        # Смотрим на зависимости указанного пакета
        package = next(p for p in installed_packages if p.project_name.lower() == package_name.lower())
        # Рекурсивно определяем зависимости
        stack = [package]

        while stack:
            current_package = stack.pop()
            for dependency in current_package.requires():
                dependencies[current_package.project_name].add(dependency.project_name)
                dependency_package = next(
                    (p for p in installed_packages if p.project_name.lower() == dependency.project_name.lower()), None)
                if dependency_package:
                    stack.append(dependency_package)
    except StopIteration:
        print(f"Package '{package_name}' not found.")

    return dependencies


def generate_plantuml(dependencies):
    """Генерируем код PlantUML для графа зависимостей."""
    uml = ['@startuml']
    for package, deps in dependencies.items():
        for dep in deps:
            uml.append(f"{package} --> {dep}")
    uml.append('@enduml')
    return "\n".join(uml)


def main():
    parser = argparse.ArgumentParser(description="Dependency Visualizer")
    parser.add_argument('path_to_program', type=str, help="Path to the program")
    parser.add_argument('package_name', type=str, help="Name of the package to analyze")
    parser.add_argument('output_file', type=str, help="Path to the output file for the PlantUML code")
    parser.add_argument('repository_url', type=str, help="URL of the repository")

    args = parser.parse_args()

    dependencies = get_dependencies(args.package_name)
    plantuml_code = generate_plantuml(dependencies)

    with open(args.output_file, 'w') as f:
        f.write(plantuml_code)

    print(plantuml_code)


if __name__ == '__main__':
    main()
