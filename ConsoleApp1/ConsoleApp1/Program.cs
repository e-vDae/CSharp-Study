using System;

class SalaryIncrease
{
    static void Main()
    {
        Console.Title = "SalaryIncreasonator";
        decimal Salary;
        decimal NewSalary;
        string Currency = "Riyals";

        Salary = 10M;
        NewSalary = SalaryIncreasonator1000();

        if (NewSalary < 9_999_999)
        {
            Console.WriteLine("\nThat's too low habibi, you still boor berson :(");
        }
        else
        {
            Console.WriteLine($"\nYour previous salary is {Salary} {Currency} :(");
            Console.WriteLine($"Your salary is now {NewSalary} {Currency}, Shukran Habibi, You rich now, Buy Lamborghini!");
        }

        Console.ReadKey();
    }
    static decimal SalaryIncreasonator1000()
    {
        Console.Write("Input your asking salary habibi : ");
        decimal HowMuchHabibi = Convert.ToDecimal(Console.ReadLine());
        return HowMuchHabibi;
    }

    static decimal SalaryIncreasonator3000()
	{
        Console.Write("Input your asking salary habibi ");
        decimal HowMuchHabibi = Convert.ToDecimal(Console.ReadLine());

        while (HowMuchHabibi < 9_999_999_999)
            {
                Console.Write("\nThat's too low habibi, add more blease... ");
                HowMuchHabibi = Convert.ToDecimal(Console.ReadLine());
            }

        return HowMuchHabibi;
    }

}