from tools.chart_tool import create_line_chart


def main():

    x_values = [
        "09-01",
        "09-02",
        "09-03",
        "09-04",
        "09-05",
    ]

    y_values = [
        1200,
        1500,
        1300,
        1800,
        2100,
    ]

    result = create_line_chart(
        x_values=x_values,
        y_values=y_values,
        title="每日销售额",
        x_label="日期",
        y_label="销售额",
    )

    print(result)


if __name__ == "__main__":
    main()
