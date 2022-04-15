using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using NUnit.Framework;
using RouteService.Logic;
using RouteService.Logic.Data;
using System;
using System.Collections.Generic;

namespace RouteService.Test
{
	public class Tests
	{
		private static ILogger? Log { get; set; } = null;

		[SetUp]
		public void Setup()
		{
			Environment.SetEnvironmentVariable("TeamsFromMailUser", "developers@esri.nl");
			Environment.SetEnvironmentVariable("TeamsClientID", "df70994a-e449-49ae-abdf-71f9e5b9e465");
			Environment.SetEnvironmentVariable("TeamsClientSecret", "Ojp7Q~l2tJ90QMEdPqt~cztOX4LZK6tVtVD43");
			Environment.SetEnvironmentVariable("TeamsTenant", "67a74277-d540-476d-a803-0c0879ee7201");

			// Create a logger. 
			ILoggerFactory loggingFactory = new NullLoggerFactory();
			Log = loggingFactory.CreateLogger("UnitTest");
		}

		[Test]
		public void Test1()
		{
			MailMessage message = new MailMessage()
			{
				SaveToSentItems = "false",
				Message = new Message()
				{
					Subject = "Automate you platform",
					Body = new Body()
					{
						ContentType = "HTML",
						Content = $"Hoi <br/> Mooie mail "
					},
					ToRecipients = new List<Recipient>() { new Recipient() { EmailAddress = new EmailAddress() { Address = "gbultje@esri.nl" } } },
					BccRecipients = new List<Recipient>() { new Recipient() { EmailAddress = new EmailAddress() { Address = "developers@esri.nl" } } },
				}
			};

			MailLogic mailLogic = new MailLogic();
			Assert.IsTrue(mailLogic.SendMail(Log, message));
		}
	}
}